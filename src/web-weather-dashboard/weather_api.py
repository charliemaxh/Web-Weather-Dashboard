from abc import ABC, abstractmethod
import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

#load variables from .env file
load_dotenv()
app = FastAPI()


class WeatherAPI(ABC):
    """
    Abstract base class for weather APIs.
    Defines the interface for fetching weather data from different services.
    """
    @abstractmethod
    def get_weather(self,location):
        """
        Abstract method to fetch weather data for a specific location.
        
        Args:
            location (str): The location for which weather data is to be fetched.
            
        Returns:
            dict: The weather data for the specified location.
        """
        pass

class OpenWeatherMapAPI(WeatherAPI):
    """
    Class for fetching weather data from the OpenWeatherMap API.
    Inherits from the WeatherAPI base class.
    """
    def __init__(self):
        """
        Initializes the OpenWeatherMapAPI class with the API key and base URL.
        """
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        print(f"[DEBUG] API Key: {self.api_key}")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather" 
        

        

    def get_weather(self, location):
        """
        Fetches weather data for a specific location using the OpenWeatherMap API.

        Args:
            location (str): The location (city name) for which weather data is to be fetched.

        Returns:
            dict: JSON response containing weather data for the location.

        Raises:
            Exception: If the API call fails or returns a non-200 status code.
        """
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        print(f"[DEBUG] API Key: {self.api_key}")  # Debug API Key
        print(f"[DEBUG] Params: {params}")  # Print parameters
        response = requests.get(self.base_url, params=params)
        print(f"[DEBUG] Full URL: {response.url}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        pass

class TomorrowAPI(WeatherAPI):
    """
    Class for fetching weather data from the WeatherAPI (Tomorrow.io) API.
    Inherits from the WeatherAPI base class.
    """
    def __init__(self):
        """
        Initializes the TomorrowAPI class with the API key and base URL.
        """
        self.api_key = os.getenv("TOMORROW_API_KEY_API_KEY")
        self.base_url = "http://api.tomorrow.io/v4/weather/realtime"
       

    def get_weather(self, location):
        """
        Fetches weather data for a specific location using the WeatherAPI (Tomorrow.io) API.

        Args:
            location (str): The location (city name) for which weather data is to be fetched.

        Returns:
            dict: JSON response containing weather data for the location.

        Raises:
            Exception: If the API call fails or returns a non-200 status code.
        """
        params = {
            "location": location,
            "apikey": self.api_key,
        }
        response = requests.get(self.base_url, params=params)
        print(f"[DEBUG] Full URL: {response.url}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data for {location}: {response.text}")
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        pass

open_weather_api = OpenWeatherMapAPI()
tomorrow_api = TomorrowAPI()

@app.get("/weather/openweathermap/{location}")
async def get_openweathermap_weather(location: str):
    """
    FastAPI endpoint to get weather data from OpenWeatherMap.
    """
    try:
        weather_data = open_weather_api.get_weather(location)
        return weather_data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.get("/weather/tomorrow/{location}")
async def get_tomorrow_weather(location: str):
    """
    FastAPI endpoint to get weather data from TomorrowAPI.
    """
    try:
        weather_data = tomorrow_api.get_weather(location)
        return weather_data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
