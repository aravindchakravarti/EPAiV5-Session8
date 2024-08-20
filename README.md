# EPAiV5-Session8

Name  : Aravind D. Chakravarti
Email : aravinddcsadguru@gmail.com

![image](https://github.com/user-attachments/assets/ce32d46d-67dc-4e4b-8832-dac7aa9604e6)


## Function Execution Timing

#### Overview

The `time_the_fun` decorator is a Python utility designed to measure the execution time of any function it decorates. By wrapping your functions with this decorator, we can easily monitor and log how long they take to run, which is useful for performance analysis and optimization.

## Random Profiles
#### Overview

The `generate_fake_profiles_and_stats_tuple` function generates a set of fake profiles and computes various statistical measures based on the generated data. This function is useful for testing, simulation, and analysis where demographic information such as age, blood type, and geographic coordinates are needed.

We generate the profiles using `Faker` library of python and store them as `namedtuples`. 
First we create a `namedtuple` instance as below
```python
# Define a named tuple for person profiles
person_profile = namedtuple('person_profile', ['age', 'lat', 'long', 'blood_type'])
```
Then we generate `10000` random profiles using `for` loop
```python
# Generate fake profiles
profiles = tuple(
	person_profile(fake.random_age(), fake.latitude(), fake.longitude(), fake.blood_group())
	for  _  in  range(num_people)
)
```
To calculate `mean` and other highest values we use generic python functions

There are two ways in which we are storing profiles. 
In `generate_fake_profiles_and_stats_tuple` we are using `tuples` to store `namedtuple` `objects`
and in `generate_fake_profiles_and_stats_dict` we are using `list` to store `dictionary` of profiles

## Stock Market Value
#### Overview

This includes two functions, `generate_companies` and `calculate_stock_market_value`, designed to simulate a stock market environment. The first function generates a list of companies with fake stock data, while the second calculates the overall market values based on the weighted average of the generated data.

```python
# Define a namedtuple for storing company stock data
CompanyStock = namedtuple('CompanyStock', ['name', 'symbol', 'open', 'high', 'close', 'weight'])
```
Above generates `namedtuple` class with parameters. And using `faker` and `random`library of python we create stock market data as below

```python
# Generate company name and symbol
name = fake.company()
symbol = ''.join(random.sample(name, 4)).upper() # Create a 4-letter symbol from the company name
 # Generate random stock prices
open_price = round(random.uniform(100, 500), 2) # Random open price between 100 and 500
high_price = round(open_price + random.uniform(0, 50), 2) # High price must be higher than open price
close_price = round(random.uniform(open_price, high_price), 2) # Close price between open and high
```
