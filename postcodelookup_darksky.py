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



#append latitude_longitude to darksky url and open it
#or use darksky api and do something with that
