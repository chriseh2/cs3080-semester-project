'''
Christopher Helland
SP26 UCCS CS3080
Semester Project - Weather App
Due: 05/03/2026
main.py

Features:
    - Input a city, output current weather using OpenWeatherMap API.
    - Add temperature conversion and GUI using tkinter for extra practice.

API docs: https://openweathermap.org/api/one-call-3?collection=one_call_api_3.0
'''

import requests

OPENWEATHERMAP_API_KEY = ""

class Location:
    def __init__(self, city, state, latitude=None, longitude=None):
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        coordinates = self.get_coordinates(self)

    @staticmethod
    def get_coordinates(self):
        """Translate plain text city and state into lat and long coords"""
        try:
            response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.state},USA&limit=1&appid={OPENWEATHERMAP_API_KEY}")
            data = response.json()
            if len(data) > 0:
                self.latitude = data[0]["lat"]
                self.longitude = data[0]["lon"]
            elif len(data) == 0:
                raise ValueError("No verified locations were found using the provided city and state.")
        except requests.exceptions.RequestException as e:
            print(f"Something went wrong: {e}")

class Weather(Location):
    def __init__(
            self, city, state,
            sunrise=None, sunset=None,
            temp=None, feels_like=None,
            pressure=None, humidity=None, dew_point=None,
            clouds=None, uvi=None, visibility=None,
            wind_speed=None, wind_gust=None, wind_deg=None,
            rain=None, snow=None, condition=None, condition_description=None
            ):
        super().__init__(city, state)
        self.sunrise = sunrise
        self.sunset = sunset
        self.temp = temp
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.dew_point = dew_point
        self.clouds = clouds
        self.uvi = uvi
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.wind_deg = wind_deg
        self.rain = rain
        self.snow = snow
        self.condition = condition
        self.condition_description = condition_description
        self.get_weather(self)
        
    @staticmethod
    def get_weather(self):
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={OPENWEATHERMAP_API_KEY}")
            data = response.json()
            self.parse_weather(data)
        except requests.exceptions.RequestException as e:
            print(f"Something went wrong: {e}")

    def parse_weather(self, data):
        #self.sunrise = sunrise
        #self.sunset = sunset
        #self.temp = temp
        #self.feels_like = feels_like
        #self.pressure = pressure
        #self.humidity = humidity
        #self.dew_point = dew_point
        #self.clouds = clouds
        #self.uvi = uvi
        #self.visibility = visibility
        #self.wind_speed = wind_speed
        #self.wind_gust = wind_gust
        #self.wind_deg = wind_deg
        #self.rain = rain
        #self.snow = snow
        self.condition = data['weather'][0]['main']
        self.condition_description = data['weather'][0]['description']

    def print(self):
        print(f"==== Forecast for {self.city}, {self.state}: ====")

if __name__=="__main__":
    # User input
    city_input = input("City: ")
    state_input = input("State: ")

    # Initialize Weather Object
    Weather = Weather(city_input, state_input)