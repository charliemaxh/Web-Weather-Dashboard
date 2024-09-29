from abc import ABC, abstractmethod
import requests
import os
from dotenv import load_dotenv

#load variables from .env file
load_dotenv()

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
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json
        else:
            raise Exception(f"Failed to fetch weather data: {response.status.code}")
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
        self.api_key = os.getenv("TOMORROW_API_KEY")
        self.base_url = "http://api.weatherapi.com/v1/"

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
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json
        else:
            raise Exception(f"Failed to fetch weather data: {response.status.code}")
        pass