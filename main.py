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

import os
import requests

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

class Location:
    def __init__(self, city, state):
        self.city = city
        self.state = state
        self.latitude = None
        self.longitude = None
        self.resolve_coordinates()

    def resolve_coordinates(self):
        url = (
            "http://api.openweathermap.org/geo/1.0/direct"
            f"?q={self.city},{self.state},USA&limit=1&appid={OPENWEATHERMAP_API_KEY}"
        )
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if not data:
            raise ValueError("No verified location found for that city/state.")

        self.latitude = data[0]["lat"]
        self.longitude = data[0]["lon"]


class Weather:
    def __init__(self, location: Location):
        self.location = location
        self.temp = None
        self.feels_like = None
        self.pressure = None
        self.humidity = None
        self.clouds = None
        self.visibility = None
        self.wind_speed = None
        self.wind_gust = None
        self.wind_deg = None
        self.condition = None
        self.condition_description = None

    def fetch(self):
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={self.location.latitude}&lon={self.location.longitude}"
            f"&appid={OPENWEATHERMAP_API_KEY}"
        )
        response = requests.get(url)
        response.raise_for_status()
        self.parse(response.json())

    def parse(self, data):
        self.temp = data["main"]["temp"]
        self.feels_like = data["main"]["feels_like"]
        self.pressure = data["main"]["pressure"]
        self.humidity = data["main"]["humidity"]
        self.clouds = data["clouds"]["all"]
        self.visibility = data.get("visibility")
        wind = data.get("wind", {})
        self.wind_speed = wind.get("speed")
        self.wind_gust = wind.get("gust")
        self.wind_deg = wind.get("deg")
        self.condition = data["weather"][0]["main"]
        self.condition_description = data["weather"][0]["description"]

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

    def print_report(self):
        print(f"Forecast for {self.location.city}, {self.location.state}:")
        print(f"  Condition: {self.condition} ({self.condition_description})")
        print(f"  Temperature: {self.temp} K ({self.k_to_f(self.temp):.2f} fahrenheit)")
        print(f"  Feels Like: {self.feels_like} kelvin ({self.k_to_f(self.feels_like):.2f} fahrenheit)")
        print(f"  Pressure: {self.pressure} hPa")
        print(f"  Humidity: {self.humidity} %")
        print(f"  Clouds: {self.clouds} %")
        print(f"  Visibility: {self.visibility} m ({self.m_to_mi(self.visibility):.2f} miles)")
        print(f"  Wind Speed: {self.wind_speed} m/s ({self.ms_to_mph(self.wind_speed):.2f} mph)")
        print(f"  Wind Gust: {self.wind_gust} m/s ({self.ms_to_mph(self.wind_gust):.2f} mph)")
        print(f"  Wind Degrees: {self.wind_deg} degrees ({self.degrees_to_direction(self.wind_deg)})")

if __name__ == "__main__":
    city_input = input("City: ")
    state_input = input("State: ")

    location = Location(city_input, state_input)
    weather = Weather(location)
    weather.fetch()
    weather.print_report()
