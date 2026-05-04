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
import os

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

class Location:
    def __init__(self, city, state, latitude=None, longitude=None):
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        coordinates = self.get_coordinates()

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
            temp=None, feels_like=None,
            pressure=None, humidity=None,
            clouds=None, visibility=None,
            wind_speed=None, wind_gust=None, wind_deg=None,
            condition=None, condition_description=None
            ):
        super().__init__(city, state)
        self.temp = temp
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.clouds = clouds
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.wind_deg = wind_deg
        self.condition = condition
        self.condition_description = condition_description
        self.get_weather()
        
    def get_weather(self):
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={OPENWEATHERMAP_API_KEY}")
            data = response.json()
            self.parse_weather(data)
            print(data)
        except requests.exceptions.RequestException as e:
            print(f"Something went wrong: {e}")

    @staticmethod
    def k_to_f(temp_K):
        return (temp_K-273.15)*(9/5)+32
    
    @staticmethod
    def m_to_mi(dist_m):
        return dist_m/1609
    
    @staticmethod
    def ms_to_mph(speed_ms):
        return speed_ms*2.237
    
    @staticmethod
    def degrees_to_direction(degrees):
        if (0 <= degrees <= 11):
            return "North (N)"
        elif (11 < degrees <= 33):
            return "North-Northeast (NNE)"
        elif (33 < degrees <= 56):
            return "Northeast (NE)"
        elif (56 < degrees <= 78):
            return "East-Northeast (ENE)"
        elif (78 < degrees <= 101):
            return "East"
        elif (101 < degrees <= 123):
            return "East-Southeast (ESE)"
        elif (123 < degrees <= 146):
            return "Southeast (SE)"
        elif (146 < degrees <= 168):
            return "South-Southeast (SSE)"
        elif (168 < degrees <= 191):
            return "South (S)"
        elif (191 < degrees <= 213):
            return "South-Southwest (SSW)"
        elif (213 < degrees <= 236):
            return "Southwest (SW)"
        elif (236 < degrees <= 258):
            return "West-Southwest (WSW)"
        elif (258 < degrees <= 281):
            return "West (W)"
        elif (281 < degrees <= 303):
            return "West-Northwest (WNW)"
        elif (303 < degrees <= 326):
            return "Northwest (NW)"
        elif (326 < degrees <= 348):
            return "North-Northwest (NNW)"
        elif (348 < degrees <= 360):
            return "North (N)"
        else:
            return "NaN"

    def parse_weather(self, data):
        self.temp = data['main']['temp']
        self.feels_like = data['main']['feels_like']
        self.pressure = data['main']['pressure']
        self.humidity = data['main']['humidity']
        self.clouds = data['clouds']['all']
        self.visibility = data['visibility']
        self.wind_speed = data['wind']['speed']
        self.wind_gust = data['wind']['gust']
        self.wind_deg = data['wind']['deg']
        self.condition = data['weather'][0]['main']
        self.condition_description = data['weather'][0]['description']

    def print_weather(self):
        print(f"Forecast for {self.city}, {self.state}:")
        print(f"      Current Condition: {self.condition} ({self.condition_description})")
        print(f"      Temperature: {self.temp} kelvin ({self.k_to_f(self.temp):.2f} fahrenheit)")
        print(f"      Feels Like: {self.feels_like} kelvin ({self.k_to_f(self.feels_like):.2f} fahrenheit)")
        print(f"      Pressure: {self.pressure} hPa")
        print(f"      Humidity: {self.humidity} %")
        print(f"      Clouds: {self.clouds} %")
        print(f"      Visibility: {self.visibility} m ({self.m_to_mi(self.visibility):.2f} miles)")
        print(f"      Wind Speed: {self.wind_speed} m/s ({self.ms_to_mph(self.wind_speed):.2f} mph)")
        print(f"      Wind Gust: {self.wind_gust} m/s ({self.ms_to_mph(self.wind_gust):.2f} mph)")
        print(f"      Wind Degrees: {self.wind_deg} degrees ({self.degrees_to_direction(self.wind_deg)})")

if __name__=="__main__":
    # User input
    city_input = input("City: ")
    state_input = input("State: ")

    # Initialize Weather Object
    Weather_object = Weather(city_input, state_input)
    Weather_object.print_weather()
