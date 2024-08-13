"""
This project/assignment contains a collection of functions that serve various purposes such as checking
the presence and length of docstrings, generating Fibonacci numbers, and counting function calls.
"""


def doc_string_check(fn):
    '''
    This function takes any arbitrary function and checks if the docstring
    of the function is at least 50 words. Else, raises a warning.
    '''
    min_words_in_doc = 50
    def doc_checker(*args: any, **kwargs: any):
        '''
        This function doesn't do anything other than counting the number of 
        characters in fn.__doc__
        '''
        copy_doc_string = str(fn.__doc__)
        doc_string_len = len(copy_doc_string.split())
        alpha_characters = len([char for char in copy_doc_string if char.isalpha()])

        # Checks if docstring present or not
        if fn.__doc__ is None:
            raise SyntaxError(f'{fn.__name__} contains no docstring')

        # Check if docstring contains sufficient words
        if doc_string_len < min_words_in_doc:
            raise SyntaxError("Docstring must contain at least 50 words")

        # Check if docstring contains only letters
        if alpha_characters < 100:
            raise SyntaxError("Docstring must contain at least a few characters")

    return doc_checker


def fibonacci_closure():
    '''
    This function returns the closure for generating the next Fibonacci numbers. 
    Function takes an argument for which the next Fibonacci number to be generated.
    Index: 1 2 3 4 5 6 7  8  9 10 ....
    Series: 0 1 1 2 3 5 8 13 21 34 55 ....
    Basically Fn = Fn-1 + Fn-2
    '''
    fn_0 = 0
    fn_1 = 1

    def next_fib(n: int = 0) -> int:
        '''
        Generates the next Fibonacci number
        '''
        if not isinstance(n, int):
            raise ValueError("Fibonacci series is defined only for integers")

        if n < 0:
            raise ValueError("Fibonacci series is defined only for positive integers")

        nonlocal fn_0
        nonlocal fn_1
        # Loop through the index+1 times for which fib to be generated
        for _ in range(n + 1):
            temp_0 = fn_0
            temp_1 = fn_1
            fn_0 = temp_1
            fn_1 = temp_0 + temp_1

        # Reset the nonlocal variables, so that variables are not persistent across function calls
        fn_0 = 0
        fn_1 = 1
        return temp_0

    return next_fib


# Declare a global variable to keep track of function call count
fn_called = {}

def fun_called_cnt_closure(fn):
    '''
    This function keeps count of how many times a function gets called
    '''
    def fn_counter(*args, **kwargs):
        '''
        This function keeps count of how many times a function is called
        '''
        # Access the global variable
        global fn_called

        # Fetch the name of function and check if already exists in dictionary
        # if not create the key in the dictionary and initialize it to zero.
        if fn.__name__ not in fn_called:
            fn_called[fn.__name__] = 0

        # Update the count
        fn_called[fn.__name__] += 1

        # Return value, which is not used
        _ = fn(*args, **kwargs)

        # Return the dictionary
        return fn_called

    return fn_counter


def fun_called_cnt_closure_ext_dict(count_keep_dict: dict) -> dict:
    '''
    This function keeps count of how many times a function gets called.
    The difference with fun_called_cnt_closure() is that this closure
    requires an external dictionary 
    '''
    def inner_function(fn):
        '''
        The closure function which accepts the function input on which 
        counter will be counted
        '''
        def fn_counter(*args: any, **kwargs: any) -> dict[str:int]:
            '''
            This function keeps count of how many times a function is called
            '''
            # Fetch the name of function and check if already exists in dictionary
            # if not create the key in the dictionary and initialize it to zero.
            if fn.__name__ not in count_keep_dict:
                count_keep_dict[fn.__name__] = 0

            # Update the count
            count_keep_dict[fn.__name__] += 1

            # Return value, which is not used
            _ = fn(*args, **kwargs)

            # Return the dictionary
            return count_keep_dict
        return fn_counter
    return inner_function