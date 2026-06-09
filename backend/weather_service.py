import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

class WeatherService:
    def __init__(self):
        self.openweathermap_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.openweathermap_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
    
    def get_current_weather(self, latitude, longitude):
        """Fetch current weather data for given coordinates"""
        try:
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.openweathermap_key,
                'units': 'metric'
            }
            response = requests.get(self.openweathermap_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rainfall': data.get('rain', {}).get('1h', 0),
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'timestamp': datetime.now().isoformat()
            }
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_forecast(self, latitude, longitude, days=7):
        """Fetch weather forecast for given coordinates"""
        try:
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.openweathermap_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list']:
                forecasts.append({
                    'timestamp': item['dt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'rainfall': item.get('rain', {}).get('3h', 0),
                    'wind_speed': item['wind']['speed'],
                    'description': item['weather'][0]['description']
                })
            
            return forecasts
        except requests.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def calculate_crop_suitability(self, temperature, humidity, rainfall):
        """Calculate crop suitability based on weather conditions"""
        # Simple scoring system
        score = 0
        factors = {}
        
        # Temperature scoring (optimal: 20-30°C for most crops)
        if 20 <= temperature <= 30:
            temp_score = 100
        elif 15 <= temperature < 20 or 30 < temperature <= 35:
            temp_score = 70
        else:
            temp_score = 30
        
        factors['temperature'] = temp_score
        
        # Humidity scoring (optimal: 60-80%)
        if 60 <= humidity <= 80:
            humidity_score = 100
        elif 50 <= humidity < 60 or 80 < humidity <= 90:
            humidity_score = 70
        else:
            humidity_score = 30
        
        factors['humidity'] = humidity_score
        
        # Rainfall scoring (seasonal dependent)
        if 20 <= rainfall <= 100:
            rainfall_score = 100
        elif 10 <= rainfall < 20 or 100 < rainfall <= 150:
            rainfall_score = 70
        else:
            rainfall_score = 30
        
        factors['rainfall'] = rainfall_score
        
        # Overall score
        overall_score = (temp_score + humidity_score + rainfall_score) / 3
        
        return {
            'overall_suitability': overall_score,
            'factors': factors,
            'recommendation': 'Good conditions for planting' if overall_score >= 70 else 'Suboptimal conditions'
        }
