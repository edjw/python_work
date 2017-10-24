""" Asks for a UK postcode, uses postcodes.io to get the latitude and longitude of that postcode, rounds the result to 4 decimal places as that's the most Dark Sky uses, and opens darksky.net to get the forecast for the longitude/latitude of that postcode. """

"""
todo
1. Use regex or postcode.io's postcode validation to check the postcode entered is a valid UK postcode and tell the user to re-enter a proper postcode
2. use darksky api and do something else with this info
"""

"""
Learnt: requests, using an API, returning values from a function, parsing JSON in python, input prompts, confidence!
"""

import requests, webbrowser

postcode = input('Enter your postcode to check the weather on DarkSky.\n')

def postcodeLookup(postcode):
    url = "https://api.postcodes.io/postcodes/"
    r = requests.get(url+postcode)
    r.raise_for_status()
    response_dict = r.json()
    latitude = round(response_dict['result']['latitude'], 4)
    longitude = round(response_dict['result']['longitude'], 4)
    result = str(latitude) + "," + str(longitude)
    return result 
latitude_longitude = postcodeLookup(postcode)

def openDarkSky(latitude_longitude):
    webbrowser.open('https://darksky.net/forecast/' + latitude_longitude + "/uk224/en")
openDarkSky(latitude_longitude)




