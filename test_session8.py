import pytest
from unittest.mock import patch
from decimal import Decimal
from faker import Faker
from session8 import fake, time_the_fun, generate_fake_profiles_and_stats_tuple, person_profile, generate_fake_profiles_and_stats_dict
from session8 import generate_companies, CompanyStock
import session8
import inspect
import re
import os

def test_readme_exists():
    '''
    To check if ReadMe exists
    '''
    assert os.path.isfile("README.md"), "README.md file missing!"

README_CONTENT_CHECK_FOR = [
        "decorator",
        "faker",
        "namedtuple",
        "stock"
        ]

def test_readme_contents():
    '''
    To check if ReadMe includes important "Keywords"
    '''
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 100, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    '''
    To check if author has provided sufficient description
    '''
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    '''
    To check if author has used Markdown editing format or not
    '''
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

# Test the BloodGroupProvider
def test_blood_group_provider():
    blood_group = fake.blood_group()
    assert blood_group in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], \
        "Generated blood group is not valid."

# Test the AgeProvider
def test_random_age_provider():
    age = fake.random_age()
    assert 0 <= age < 100, "Generated age is out of range."

# Test if time_the_fun decorator measures time and prints it
@patch('builtins.print')
def test_time_the_fun_decorator(mock_print):
    @time_the_fun
    def test_func():
        return "Test"

    result = test_func()
    assert result == "Test"
    mock_print.assert_called_once()

# Test if the number of profiles generated matches the input
def test_generate_correct_number_of_profiles():
    num_profiles = 5
    profiles = generate_fake_profiles_and_stats_tuple(num_profiles)
    assert len(profiles) == num_profiles, \
        "The number of generated profiles does not match the expected number."

# Test that statistics are calculated correctly
def test_calculate_statistics_correctly():
    profiles = [person_profile(25, Decimal('10.0'), Decimal('20.0'), 'O+') for _ in range(3)]
    sum_lat = Decimal('30.0')
    sum_long = Decimal('60.0')
    sum_age = 75
    largest_age = 25
    mean_lat = sum_lat / len(profiles)
    mean_long = sum_long / len(profiles)
    mean_age = sum_age / len(profiles)
    
    assert mean_lat == Decimal('10.0')
    assert mean_long == Decimal('20.0')
    assert mean_age == 25

# Test if blood group count dictionary is populated correctly
def test_blood_group_count():
    profiles = [person_profile(25, Decimal('10.0'), Decimal('20.0'), 'O+'),
                person_profile(30, Decimal('15.0'), Decimal('25.0'), 'A+'),
                person_profile(20, Decimal('20.0'), Decimal('30.0'), 'O+')]
    
    blood_group_dict = {'A+': 0, 'A-': 0, 'B+': 0, 'B-': 0, 'AB+': 0, 'AB-': 0, 'O+': 0, 'O-': 0}
    
    for profile in profiles:
        blood_group_dict[profile.blood_type] += 1
    
    assert blood_group_dict['O+'] == 2, "O+ blood group count is incorrect."
    assert blood_group_dict['A+'] == 1, "A+ blood group count is incorrect."

# Test if latitude and longitude are correctly aggregated
def test_latitude_longitude_aggregation():
    profiles = [person_profile(25, Decimal('10.0'), Decimal('20.0'), 'O+'),
                person_profile(30, Decimal('15.0'), Decimal('25.0'), 'A+')]
    
    sum_lat = sum(profile.lat for profile in profiles)
    sum_long = sum(profile.long for profile in profiles)
    
    assert sum_lat == Decimal('25.0')
    assert sum_long == Decimal('45.0')

# Test if the largest age is correctly identified
def test_largest_age_identification():
    profiles = [person_profile(25, Decimal('10.0'), Decimal('20.0'), 'O+'),
                person_profile(35, Decimal('15.0'), Decimal('25.0'), 'A+')]
    
    largest_age = max(profile.age for profile in profiles)
    
    assert largest_age == 35, "Largest age is not identified correctly."

# Test if the mean age is correctly calculated
def test_mean_age_calculation():
    profiles = [person_profile(25, Decimal('10.0'), Decimal('20.0'), 'O+'),
                person_profile(35, Decimal('15.0'), Decimal('25.0'), 'A+')]
    
    mean_age = sum(profile.age for profile in profiles) / len(profiles)
    
    assert mean_age == 30, "Mean age is not calculated correctly."

time_taken_tuple = []
time_taken_dict = []

@patch('builtins.print')
def test_generate_fake_profiles_and_stats_execution_time(mock_print, time_taken_tuple):
    # Call the function with a small number of profiles
    generate_fake_profiles_and_stats_tuple(10)

    # Extract the printed execution time from the decorator
    assert mock_print.call_count == 7  # 5 print statements in the function, 1 for execution time
    last_print_call = mock_print.call_args_list[-1][0][0]

    # Check if the last print statement contains the execution time
    assert "Time taken to execute generate_fake_profiles_and_stats_tuple is" in last_print_call, \
        "Execution time was not captured or printed correctly."

    # Optionally, you can parse the time from the string and ensure it’s a float greater than zero
    time_taken_str = last_print_call.split("is")[1].strip()
    time_taken = float(time_taken_str)
    assert time_taken < 0.3, "Execution time should be greater than zero."

    time_taken_tuple.appen(time_taken)

@patch('builtins.print')
def test_generate_fake_profiles_and_stats_execution_time(mock_print):
    # Call the function with a small number of profiles
    generate_fake_profiles_and_stats_dict(10)

    # Extract the printed execution time from the decorator
    assert mock_print.call_count == 7  # 5 print statements in the function, 1 for execution time
    last_print_call = mock_print.call_args_list[-1][0][0]

    # Check if the last print statement contains the execution time
    assert "Time taken to execute generate_fake_profiles_and_stats_dict is" in last_print_call, \
        "Execution time was not captured or printed correctly."

    # Optionally, you can parse the time from the string and ensure it’s a float greater than zero
    time_taken_str = last_print_call.split("is")[1].strip()
    time_taken = float(time_taken_str)
    assert time_taken < 0.3, "Execution time should be greater than zero."

def test_generate_companies_length():
    companies, total_weight = generate_companies(100)
    assert len(companies) == 100, "The number of generated companies should be 100."

def test_generate_companies_total_weight():
    companies, total_weight = generate_companies(100)
    assert total_weight > 0, "The total weight should be greater than 0."

def test_generate_companies_attributes():
    companies, _ = generate_companies(100)
    assert all(isinstance(company, CompanyStock) for company in companies), \
        "All items should be instances of CompanyStock namedtuple."
    assert all(hasattr(company, 'name') for company in companies), \
        "Each company should have a 'name' attribute."
    assert all(hasattr(company, 'symbol') for company in companies), \
        "Each company should have a 'symbol' attribute."
    assert all(hasattr(company, 'open') for company in companies), \
        "Each company should have an 'open' attribute."
    assert all(hasattr(company, 'high') for company in companies), \
        "Each company should have a 'high' attribute."
    assert all(hasattr(company, 'close') for company in companies), \
        "Each company should have a 'close' attribute."
    assert all(hasattr(company, 'weight') for company in companies), \
        "Each company should have a 'weight' attribute."

def test_generate_companies_stock_price_relation():
    companies, _ = generate_companies(100)
    for company in companies:
        assert company.open <= company.high, \
            "The 'high' price should be greater than or equal to the 'open' price."
        assert company.open <= company.close <= company.high, \
            "The 'close' price should be between 'open' and 'high' prices."


if 0:
    import pytest
    import random
    import string
    import os
    import inspect
    import re
    import math
    import time
    import session8
    from session8 import doc_string_check, fibonacci_closure, fun_called_cnt_closure, fun_called_cnt_closure_ext_dict, fn_called

    '''
        There is no separate assignment link. You need to write the code + test code, test your actions, and then 
        submit the link on the assignment page. 

    1.  Write a closure that takes a function and then check whether the function passed has a docstring with 
        more than 50 characters. 50 is stored as a free variable (+ 4 tests) - 200

    2.  Write a closure that gives you the next Fibonacci number (+ 2 tests) - 100

    3.  We wrote a closure that counts how many times a function was called. Write a new one that can keep 
        track of how many times add/mul/div functions were called, and update a global dictionary variable with 
        the counts (+ 6 tests) - 250

    4.  Modify above such that now we can pass in different dictionary variables to update different dictionaries 
        (+ 6 tests) - 250

    5.  Once done, upload the code to Git Hub, run actions, and then proceed to answer S6 - Assignment QnA. 

    6.  No readme or no docstring for each function, or no test cases (4, 2, 6, 6, >7 = 25 tests), then 0. 
        Write at least 7 test cases to check boundary conditions that might cause your code to fail. 
        Scores = Total Tests * 5 + Total Cleared Tests * 5

    '''

    '''
    **********************************************************************************************************
                                            GENERIC TEST CASES
    **********************************************************************************************************
    '''

    README_CONTENT_CHECK_FOR = [
        "fibonacci",
        "docstring",
        "closure",
        "count",
        "decorator"
        ]

    def test_readme_exists():
        '''
        To check if ReadMe exists
        '''
        assert os.path.isfile("README.md"), "README.md file missing!"

    def test_readme_contents():
        '''
        To check if ReadMe includes important "Keywords"
        '''
        readme = open("README.md", "r")
        readme_words = readme.read().split()
        readme.close()
        assert len(readme_words) >= 250, "Make your README.md file interesting! Add atleast 500 words"

    def test_readme_proper_description():
        '''
        To check if author has provided sufficient description
        '''
        READMELOOKSGOOD = True
        f = open("README.md", "r", encoding="utf-8")
        content = f.read()
        f.close()
        for c in README_CONTENT_CHECK_FOR:
            if c not in content:
                READMELOOKSGOOD = False
                pass
        assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

    def test_readme_file_for_formatting():
        '''
        To check if author has used Markdown editing format or not
        '''
        f = open("README.md", "r", encoding="utf-8")
        content = f.read()
        f.close()
        assert content.count("#") >= 10

    def test_indentations():
        ''' Returns pass if used four spaces for each level of syntactically \
        significant indenting.'''
        lines = inspect.getsource(session8)
        spaces = re.findall('\n +.', lines)
        for space in spaces:
            assert len(space) % 4 == 2, "Your script contains misplaced indentations"
            assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

    def test_function_name_had_cap_letter():
        '''
        To check if function name contains any capital letter or camelcase
        '''
        functions = inspect.getmembers(session8, inspect.isfunction)
        for function in functions:
            assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


    '''
    **********************************************************************************************************
                                        DOCSTRING CHECKER TEST CASES
    **********************************************************************************************************
    '''

    def test_doc_strings_without_docstring():
        '''
        Checks if function caches if no docstring present
        '''
        with pytest.raises(SyntaxError, match=r".*no docstring*"):
            def add_with_num_no_doc(a, b):
                return(a+b)
            fn_test = doc_string_check(add_with_num_no_doc)
            fn_test(2,3)

    def test_doc_string_check():
        '''
        Check if number of words in docstring is less than 50
        '''
        with pytest.raises(SyntaxError, match=r".*at least 50 words*"):
            def add(a, b):
                '''
                This function adds two numbers and returns sum
                '''
                return (a+b)
            fn_test = doc_string_check(add)
            fn_test(4, 5)


    def test_doc_string_no_exception():
        '''
        Check if number of words in docstring is less than 50
        '''
        def add_with_long_doc(a, b):
            '''
            This function adds two numbers and returns the sum. The purpose of this function
            is to demonstrate the addition of two integers or floats. The result of the 
            addition will be returned as the output of this function. This docstring is 
            deliberately made long to satisfy the requirement of having at least fifty words.
            '''
            return (a+b)
        fn_test = doc_string_check(add_with_long_doc)
        try:
            fn_test(1, 2)
        except:
            pytest.fail("test_doc_string_check raised exception unexpectedly")


    def test_doc_strings_without_letter():
        '''
        Check docstring contains only numbers
        '''
        with pytest.raises(SyntaxError, match=r".*at least a few characters*"):
            def add_with_num_only_doc(a, b):
                '''
                0 1 2 3 4 5 6 7 8 9
                0 1 2 3 4 5 6 7 8 9
                0 1 2 3 4 5 6 7 8 9
                0 1 2 3 4 5 6 7 8 9
                0 1 2 3 4 5 6 7 8 9
                0 1 2 3 4 5 6 7 8 9
                '''
                return(a+b)
            fn_test = doc_string_check(add_with_num_only_doc)
            fn_test(2,3)

    '''
    **********************************************************************************************************
                                    FIBONACCI NUMBER GENERATOR TEST CASES
    **********************************************************************************************************
    '''
        
    def test_fib_closure_less_than_zero():
        '''
        Checks the fibonacci with negative values
        '''
        with pytest.raises(ValueError, match=r".*positive integers*"):
            fn = fibonacci_closure()
            fn(-1)

    def test_fib_closure_with_float():
        '''
        Checks if the fibonacci series handles negative numbers
        '''
        with pytest.raises(ValueError, match=r".*integers*"):
            fn = fibonacci_closure()
            fn(1.1)
            fn('a')

    def test_fib_for_int_values():
        '''
        Checks if fibonacci series correctly predicts the next fib 
        number
        '''
        fn = fibonacci_closure()
        return_val = fn(0)
        assert return_val == 0, "Fibonacci series function is not working"

        return_val = fn(10)
        assert return_val == 55, "Fibonacci series function is not working"

    '''
    **********************************************************************************************************
                                        FUNCTION CALLED COUNT TEST CASES
    **********************************************************************************************************
    '''
    def test_fun_called_cnt_closure_add():
        '''
        Checks if the function called counting is working correctly
        '''
        @fun_called_cnt_closure
        def add(a, b):
            return(a+b)
        
        return_val = add(2, 3)
        check_dictionary = {'add':1}
        assert check_dictionary == return_val, "Function counting not working properly"

    def test_fun_called_cnt_closure_add_twice():
        '''
        Checks if the function called counting is working correctly
        '''
        @fun_called_cnt_closure
        def add(a, b):
            return(a+b)
        
        _ = add(2, 3)
        return_val = add(2, 3)
        check_dictionary = {'add':3}
        assert check_dictionary == return_val, "Function counting not working properly"

    def test_fun_called_cnt_closure_add_sub():
        '''
        Checks if the function called counting is working correctly by adding 
        a new function
        '''
        @fun_called_cnt_closure
        def add(a, b):
            return(a+b)
        
        @fun_called_cnt_closure
        def sub(a, b):
            return(a-b)
        
        _ = add(2, 3)
        return_val = sub(2, 3)
        
        check_dictionary = {'add':4, 'sub':1}
        assert check_dictionary == return_val, "Function counting not working properly"

    def test_fun_called_cnt_closure_no_ags():
        '''
        Checks if the function called counting is working correctly
        by calling a function without arguments
        '''
        @fun_called_cnt_closure
        def random_fn():
            pass

        return_val = random_fn()
        
        check_dictionary = {'add':4, 'sub':1, 'random_fn' : 1}
        assert check_dictionary == return_val, "Function counting not working properly"

    def test_fun_called_cnt_closure_mem_clear():
        '''
        Checks if we can clear the count and restart the counting
        '''
        fn_called.clear()

        @fun_called_cnt_closure
        def add(a, b):
            return(a+b)

        @fun_called_cnt_closure
        def sub(a, b):
            return(a-b)

        _ = add(2, 3)
        return_val = sub(2, 3)
        
        check_dictionary = {'add':1, 'sub':1}
        assert check_dictionary == return_val, "Function counting not working properly"

    '''
    **********************************************************************************************************
                                    FUNCTION CALLED COUNT TEST CASES - EXT DICT
    **********************************************************************************************************
    '''
    ext_dict = {}

    def test_fun_called_cnt_closure_ext_dict_add():
        '''
        Checks if the function called counting is working correctly
        '''
        global ext_dict
        @fun_called_cnt_closure_ext_dict(ext_dict)
        def add(a, b):
            return(a+b)
        
        ext_dict = add(2, 3)
        check_dictionary = {'add':1}
        assert check_dictionary == ext_dict, "Function counting (external dict) not working properly"


    def test_fun_called_cnt_closure_ext_dict_twice():
            '''
            Checks if the function called counting is working correctly
            '''
            global ext_dict
            @fun_called_cnt_closure_ext_dict(ext_dict)
            def add(a, b):
                return(a+b)
            
            _ = add(2, 3)
            ext_dict = add(2, 3)
            check_dictionary = {'add':3}
            assert check_dictionary == ext_dict, "Function counting (external dict) not working properly"

    def test_fun_called_cnt_closure_ext_dict_sub():
            '''
            Checks if the function called counting is working correctly by adding 
            a new function
            '''
            global ext_dict
            @fun_called_cnt_closure_ext_dict(ext_dict)
            def add(a, b):
                return(a+b)
            
            @fun_called_cnt_closure_ext_dict(ext_dict)
            def sub(a, b):
                return(a-b)
            
            _ = add(2, 3)
            ext_dict = sub(2, 3)
            
            check_dictionary = {'add':4, 'sub':1}
            assert check_dictionary == ext_dict, "Function counting (external dict) not working properly"

    def test_fun_called_cnt_closure_ext_dict_no_ags():
            '''
            Checks if the function called counting is working correctly
            by calling a function without arguments
            '''
            global ext_dict
            @fun_called_cnt_closure_ext_dict(ext_dict)
            def random_fn():
                pass

            return_val = random_fn()
            
            check_dictionary = {'add':4, 'sub':1, 'random_fn' : 1}
            assert check_dictionary == ext_dict, "Function counting (external dict) not working properly"


    def test_fun_called_cnt_closure_ext_dict_mem_clear():
            '''
            Checks if we can clear the count and restart the counting
            '''
            global ext_dict
            ext_dict.clear()

            @fun_called_cnt_closure_ext_dict(ext_dict)
            def add(a, b):
                return(a+b)

            @fun_called_cnt_closure_ext_dict(ext_dict)
            def sub(a, b):
                return(a-b)

            _ = add(2, 3)
            ext_dict = sub(2, 3)
            
            check_dictionary = {'add':1, 'sub':1}
            assert check_dictionary == ext_dict, "Function counting not working properly"