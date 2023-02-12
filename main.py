"""Application that checks the current ISS position and lets me know if it is within viewing distance at night"""

import time
import requests
import ephem
import creds



MY_LAT = 52.133213

MY_LONG = -106.670044


# TODO: Function to check if the ISS is near my location
# Define the observer's location
observer = ephem.Observer()
observer.lat = MY_LAT # Latitude of the observer's location (in degrees)
observer.lon = MY_LONG # Longitude of the observer's location (in degrees)
observer.elevation = 0 # Elevation of the observer's location (in meters)

sat_data = requests.get("https://tle.ivanstanojevic.me/api/tle/25544").json()

sat_name = sat_data["name"]
sat_line_1 = sat_data["line1"]
sat_line_2 = sat_data["line2"]

print(sat_name)
print(sat_line_1)
print(sat_line_2)

iss = ephem.readtle(sat_name, sat_line_1, sat_line_2)


def iss_is_near():
    """Check if the ISS is near my location"""
    # Get the ISS's location
    iss.compute(observer)
    # Get the ISS's altitude
    iss_altitude = iss.alt
    # Check if the ISS is above 0 degrees
    if iss_altitude > 0:
        return True
    else:
        return False





# TODO: Function to check if the time is night for me
def is_night():
    """Check if the time is night for me"""
    # Get the sun's location
    sun = ephem.Sun()
    sun.compute(observer)
    # Get the sun's altitude
    sun_altitude = sun.alt
    # Check if the sun is below -0 degrees
    if sun_altitude < 0:
        return True
    else:
        return False

# TODO: FUnction to check if the skies are clear in my location
def is_clear():
    """Check if the skies are clear in my location"""
    # Get the weather data
    weather_data_response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,daily,alerts&appid={}".format(MY_LAT, MY_LONG, "API_KEY"))
    weather_data_response.raise_for_status() # raise an exception if the status code is not 200
    weather_data = weather_data_response.json()
    # Check if the weather data has clouds
    if weather_data["hourly"][0]["clouds"] == 0: # 0 means no clouds
        return True
    else:
        return False

print(is_clear())