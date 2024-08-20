from faker import Faker
from faker.providers import BaseProvider  # Import BaseProvider for custom providers
from collections import namedtuple
import random
from decimal import Decimal
from time import perf_counter


class BloodGroupProvider(BaseProvider):
    """
    Custom provider for generating random blood groups.

    This provider adds the ability to generate random blood groups
    from a predefined list of common blood types.
    """

    def blood_group(self):
        """
        Generate a random blood group.

        Returns:
            str: A randomly selected blood group from the list.
        """
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        return random.choice(blood_groups)


class AgeProvider(BaseProvider):
    """
    Custom provider for generating random ages.

    This provider adds the ability to generate random ages
    from 0 to 99.
    """

    def random_age(self):
        """
        Generate a random age.

        Returns:
            int: A randomly selected age from the range of 0 to 99.
        """
        ages = range(0,100, 1)
        return random.choice(ages)


# Initialize the Faker object
fake = Faker()

# Add the custom blood group and age providers to the Faker instance
fake.add_provider(BloodGroupProvider)
fake.add_provider(AgeProvider)

# Define a named tuple for person profiles
person_profile = namedtuple('person_profile', ['age', 'lat', 'long', 'blood_type'])

def time_the_fun(fn):
    """
    Decorator function to measure the execution time of a function.

    Args:
        fn (callable): The function to be timed.

    Returns:
        callable: The decorated function that measures the execution time.
    """
    def inner(*args, **kwargs):
        start = perf_counter()
        return_fn = fn(*args, **kwargs)
        stop = perf_counter()
        print(f'Time taken to execute {fn.__name__} is {stop-start}')
        return return_fn
    return inner


@time_the_fun
def generate_fake_profiles_and_stats_tuple(num_people: int):
    """
    Generate fake profiles and compute statistics.

    This function generates a specified number of fake profiles,
    calculates the mean latitude, mean longitude, mean age, largest
    age, and counts the occurrences of each blood type.

    Args:
        num_people (int): The number of fake profiles to generate.

    Prints:
        - Largest blood type by count
        - Mean latitude
        - Mean longitude
        - Largest age
        - Mean age
        - Count of each blood type
    """
    # Generate fake profiles
    profiles = tuple(
        person_profile(fake.random_age(), fake.latitude(), fake.longitude(), fake.blood_group())
        for _ in range(num_people)
    )

    # Initialize accumulators for statistics
    sum_lat = Decimal('0')
    sum_long = Decimal('0')
    sum_age = 0
    largest_age = 0
    blood_group_dict = {'A+': 0, 'A-': 0, 'B+': 0, 'B-': 0, 'AB+': 0, 'AB-': 0, 'O+': 0, 'O-': 0}

    # Calculate statistics from profiles
    for profile in profiles:
        sum_lat += profile.lat
        sum_long += profile.long
        sum_age += profile.age
        if profile.age > largest_age:
            largest_age = profile.age
        blood_group_dict[profile.blood_type] += 1

    # Calculate means
    mean_lat = sum_lat / len(profiles)
    mean_long = sum_long / len(profiles)
    mean_age = sum_age / len(profiles)

    # Print statistics
    print(f'Largest blood type = {sorted(blood_group_dict.items(), key=lambda item: item[1], reverse=True)[0][0]}')
    print(f'Mean latitude = {mean_lat}')
    print(f'Mean longitude = {mean_long}')
    print(f'Largest age = {largest_age}')
    print(f'Mean age = {mean_age}')
    print(blood_group_dict)

    return profiles


@time_the_fun
def generate_fake_profiles_and_stats_dict(num_people: int):
    """
    Generate fake profiles and compute statistics.

    This function generates a specified number of fake profiles,
    calculates the mean latitude, mean longitude, mean age, largest
    age, and counts the occurrences of each blood type.

    Args:
        num_people (int): The number of fake profiles to generate.

    Prints:
        - Largest blood type by count
        - Mean latitude
        - Mean longitude
        - Largest age
        - Mean age
        - Count of each blood type
    """
    # Generate fake profiles as a list of dictionaries
    profiles = [{
        'age': fake.random_age(),
        'lat': fake.latitude(),
        'long': fake.longitude(),
        'blood_type': fake.blood_group()
    } for _ in range(num_people)]

    # Initialize accumulators for statistics
    sum_lat = Decimal('0')
    sum_long = Decimal('0')
    sum_age = 0
    largest_age = 0
    blood_group_dict = {'A+': 0, 'A-': 0, 'B+': 0, 'B-': 0, 'AB+': 0, 'AB-': 0, 'O+': 0, 'O-': 0}

    # Calculate statistics from profiles
    for index in range(len(profiles)):
        sum_lat += profiles[index]['lat']
        sum_long += profiles[index]['long']
        sum_age += profiles[index]['age']
        if profiles[index]['age'] > largest_age:
            largest_age = profiles[index]['age']
        blood_group_dict[profiles[index]['blood_type']] += 1

    # Calculate means
    mean_lat = sum_lat / len(profiles)
    mean_long = sum_long / len(profiles)
    mean_age = sum_age / len(profiles)

    # Print statistics
    print(f'Largest blood type = {sorted(blood_group_dict.items(), key=lambda item: item[1], reverse=True)[0][0]}')
    print(f'Mean latitude = {mean_lat}')
    print(f'Mean longitude = {mean_long}')
    print(f'Largest age = {largest_age}')
    print(f'Mean age = {mean_age}')
    print(blood_group_dict)

# Define a namedtuple for storing company stock data
CompanyStock = namedtuple('CompanyStock', ['name', 'symbol', 'open', 'high', 'close', 'weight'])

# Generate stock data for 100 companies
def generate_companies(num_companies=100):
    """
    Generate fake stock data for a specified number of companies.

    Args:
        num_companies (int): The number of companies to generate data for. Default is 100.

    Returns:
        list: A list of CompanyStock namedtuples containing the company name, symbol,
              open price, high price, close price, and assigned weight.
        float: The total weight of all companies combined.
    """
    companies = []
    total_weight = 0

    for _ in range(num_companies):
        # Generate company name and symbol
        name = fake.company()
        symbol = ''.join(random.sample(name, 4)).upper()  # Create a 4-letter symbol from the company name

        # Generate random stock prices
        open_price = round(random.uniform(100, 500), 2)  # Random open price between 100 and 500
        high_price = round(open_price + random.uniform(0, 50), 2)  # High price must be higher than open price
        close_price = round(random.uniform(open_price, high_price), 2)  # Close price between open and high

        # Assign a random weight
        weight = random.uniform(0.5, 2.0)
        total_weight += weight

        # Append company data to the list
        companies.append(CompanyStock(name, symbol, open_price, high_price, close_price, weight))

    return companies, total_weight


# Calculate the stock market values
def calculate_stock_market_value(companies, total_weight):
    """
    Calculate the stock market's open, high, and close values based on the weighted average
    of each company's stock prices.

    Args:
        companies (list): A list of CompanyStock namedtuples containing stock data for each company.
        total_weight (float): The sum of the weights of all companies.

    Returns:
        tuple: A tuple containing the open market value, high market value, and close market value.
    """
    open_market_value = sum(company.open * company.weight for company in companies) / total_weight
    high_market_value = sum(company.high * company.weight for company in companies) / total_weight
    close_market_value = sum(company.close * company.weight for company in companies) / total_weight
    return open_market_value, high_market_value, close_market_value


# Generate the companies and calculate the market values
companies, total_weight = generate_companies(100)
open_market_value, high_market_value, close_market_value = calculate_stock_market_value(companies, total_weight)