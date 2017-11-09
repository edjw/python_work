import requests, webbrowser

"""
* Asks for a UK postcode
* uses postcodes.io to validate that postcode
* uses postcodes.io to get the latitude and longitude of that postcode
* rounds the result to 4 decimal places as that's the most Dark Sky uses
* opens darksky.net to get the forecast for the longitude/latitude of that postcode
"""

"""
todo
1.use darksky api and do something else with this info
"""

"""
Learnt: requests, using an API, returning values from a function, parsing JSON in python, input prompts, prompting input after invalid user response, confidence!
"""


def getUserPostcode():
    """ Get the user to submit a UK postcode """
    postcode = str(input('Enter your UK postcode to check the weather on DarkSky.\n'))
    postcode = postcode.upper() #lower case postcodes don't work on postcodes.io's API for some reason 
    return postcode
postcode = getUserPostcode()

url = "https://api.postcodes.io/postcodes/"

def postcodeValidation(postcode):
    """ Send the postcode to Postcode.io's api to check it's a valid postcode """
    r = requests.get(url + postcode + "/validate")
    response_dict = r.json() 
    if response_dict["result"] == True:
        return 'True'
    elif response_dict["result"] == False:
        return 'False'
postcode_valid = postcodeValidation(postcode)

if postcode_valid == 'True': #If the postcode is valid then skip to the lookup stage
    pass
else: #If the postcode's invalid then get the user to write a valid one
    postcode = input("Sorry that's not a real UK postcode. Try again.\n")

def postcodeLookup(postcode):
    """ Submits the postcode to Postcode.io's API and returns a string of latitude, longitude """
    r = requests.get(url + postcode)
    response_dict = r.json()
    latitude = round(response_dict['result']['latitude'], 4) #rounds the response to just 4 decimal places as that's all the DarkSky takes
    longitude = round(response_dict['result']['longitude'], 4)
    result = str(latitude) + "," + str(longitude)
    return result

latitude_longitude = postcodeLookup(postcode)

def openDarkSky(latitude_longitude):
    """ Open up darksky.net with the latitude and longitude already in there """
    webbrowser.open('https://darksky.net/forecast/' + latitude_longitude + "/uk212/en")
openDarkSky(latitude_longitude)




