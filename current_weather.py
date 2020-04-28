'''
This is a simple program to get current weather info based on user's location.
'''

import sys
import geocoder
import requests
import config

def get_city():
    '''
    This function provides user's city based on its IP address.
    If the result is not correct, asks the user to input the city.

    Returns: City name.
    '''

    # Returns user's city based on its IP address
    city_by_ip = geocoder.ip('me').city

    # Validates if the city based on the IP address is correct
    print('Are you in {}?'.format(city_by_ip))
    check = input('Please enter yes or no: ').lower()

    # Gets user's actual city
    if check == 'yes':
        actual_city = city_by_ip
    else:
        actual_city = input('Please enter the name of the city you are in: ')

    # Returns actual city
    return actual_city

def kelvin_to_celsius(temperature):
    '''
    This function converts the temperature from Kelvin to Celsius.
    Returns: Temperature in degree Celsius.
    '''

    return round(temperature - 273.15, 1)

def get_weather_conditions():
    '''
    This function returns the actual weather conditions of a user's current city
    Returns: Weather condition, temperature, feels like temperature and humidity
    '''

    # Consolidates the request's parameters
    url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = config.api_key
    city = get_city()
    payload = {'q': city, 'appid': api_key}

    # Executes the request and verifies if it was sucessful

    try:
        response = requests.request("GET", url, params=payload)
        response.raise_for_status()
    # Handles a HTTP error exception
    except requests.exceptions.HTTPError:
        print("A HTTP error has occurred! Try again later!\n")
        sys.exit(1)
    # Handles a connection exception
    except requests.exceptions.ConnectionError:
        print("A connection error has occurred! Try again later!\n")
        sys.exit(1)

    # Assigns request's results to variables
    description = response.json()['weather'][0]['description']
    temperature = kelvin_to_celsius(response.json()['main']['temp'])
    feels_like = kelvin_to_celsius(response.json()['main']['feels_like'])
    humidity = response.json()['main']['humidity']

    # Shows the results to the user
    print(f"\nCurrent weather conditions for {city}:")
    print(f"\n\tDescription: {description}\n\tTemperature: {temperature} °C"
          f"\n\tFeels like: {feels_like} °C\n\tHumidity: {humidity} %\n")

if __name__ == "__main__":
    get_weather_conditions()
