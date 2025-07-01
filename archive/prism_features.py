#!/usr/bin/env python3
"""
Prism AI Voice Assistant - Features Module
Provides weather, news, reminders, and other home assistant capabilities
"""

import os
import json
import requests
import datetime
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

@dataclass
class WeatherInfo:
    """Weather information data structure"""
    temperature: float
    condition: str
    humidity: int
    wind_speed: float
    location: str
    forecast: List[Dict[str, Any]]

@dataclass
class NewsItem:
    """News item data structure"""
    title: str
    description: str
    url: str
    source: str
    published_at: str

@dataclass
class Reminder:
    """Reminder data structure"""
    id: str
    title: str
    datetime: datetime
    completed: bool = False

class PrismFeatures:
    """Main features class for Prism AI Voice Assistant"""
    
    def __init__(self):
        self.reminders: List[Reminder] = []
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
    def get_weather(self, location: str = "auto") -> WeatherInfo:
        """Get current weather information"""
        try:
            if location == "auto":
                location = "New York"  # Default fallback
            
            if not self.weather_api_key:
                # Return mock weather data if no API key
                return WeatherInfo(
                    temperature=72.5,
                    condition="Partly Cloudy",
                    humidity=65,
                    wind_speed=8.5,
                    location=location,
                    forecast=[
                        {"day": "Today", "high": 75, "low": 68, "condition": "Partly Cloudy"},
                        {"day": "Tomorrow", "high": 78, "low": 70, "condition": "Sunny"},
                        {"day": "Wednesday", "high": 72, "low": 65, "condition": "Rainy"}
                    ]
                )
            
            # Real weather API call
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'imperial'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return WeatherInfo(
                    temperature=data['main']['temp'],
                    condition=data['weather'][0]['description'],
                    humidity=data['main']['humidity'],
                    wind_speed=data['wind']['speed'],
                    location=location,
                    forecast=self._get_weather_forecast(location)
                )
            else:
                raise Exception(f"Weather API error: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error getting weather: {e}")
            # Return fallback data
            return WeatherInfo(
                temperature=70.0,
                condition="Unknown",
                humidity=50,
                wind_speed=5.0,
                location=location,
                forecast=[]
            )
    
    def _get_weather_forecast(self, location: str) -> List[Dict[str, Any]]:
        """Get weather forecast for the next few days"""
        try:
            if not self.weather_api_key:
                return []
            
            url = f"http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'imperial'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                forecast = []
                days = {}
                
                for item in data['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in days:
                        days[date] = {
                            'day': datetime.fromtimestamp(item['dt']).strftime('%A'),
                            'high': item['main']['temp_max'],
                            'low': item['main']['temp_min'],
                            'condition': item['weather'][0]['description']
                        }
                        if len(days) >= 5:  # Get 5 days
                            break
                
                return list(days.values())
            else:
                return []
                
        except Exception as e:
            print(f"Error getting forecast: {e}")
            return []
    
    def get_news(self, category: str = "general", limit: int = 5) -> List[NewsItem]:
        """Get latest news articles"""
        try:
            if not self.news_api_key:
                # Return mock news data if no API key
                return [
                    NewsItem(
                        title="AI Breakthrough in Medical Diagnosis",
                        description="Researchers develop new AI system that can detect early signs of disease with 95% accuracy.",
                        url="https://example.com/news1",
                        source="Tech News",
                        published_at="2024-01-15T10:30:00Z"
                    ),
                    NewsItem(
                        title="Global Climate Summit Reaches Historic Agreement",
                        description="World leaders agree on ambitious new targets to reduce carbon emissions by 2030.",
                        url="https://example.com/news2",
                        source="World News",
                        published_at="2024-01-15T09:15:00Z"
                    ),
                    NewsItem(
                        title="SpaceX Successfully Launches New Satellite Constellation",
                        description="Company deploys 60 new satellites as part of global internet coverage plan.",
                        url="https://example.com/news3",
                        source="Science Daily",
                        published_at="2024-01-15T08:45:00Z"
                    )
                ]
            
            # Real news API call
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'country': 'us',
                'category': category,
                'apiKey': self.news_api_key,
                'pageSize': limit
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                news_items = []
                for article in data.get('articles', []):
                    news_items.append(NewsItem(
                        title=article.get('title', 'No title'),
                        description=article.get('description', 'No description'),
                        url=article.get('url', ''),
                        source=article.get('source', {}).get('name', 'Unknown'),
                        published_at=article.get('publishedAt', '')
                    ))
                return news_items
            else:
                raise Exception(f"News API error: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error getting news: {e}")
            return []
    
    def add_reminder(self, title: str, time_str: str) -> Reminder:
        """Add a new reminder"""
        try:
            # Parse time string (e.g., "tomorrow at 3pm", "in 2 hours", "next Monday at 10am")
            reminder_time = self._parse_time_string(time_str)
            
            reminder = Reminder(
                id=f"reminder_{len(self.reminders) + 1}",
                title=title,
                datetime=reminder_time
            )
            
            self.reminders.append(reminder)
            return reminder
            
        except Exception as e:
            print(f"Error adding reminder: {e}")
            raise
    
    def get_reminders(self, include_completed: bool = False) -> List[Reminder]:
        """Get all reminders"""
        if include_completed:
            return self.reminders
        else:
            return [r for r in self.reminders if not r.completed]
    
    def complete_reminder(self, reminder_id: str) -> bool:
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder.id == reminder_id:
                reminder.completed = True
                return True
        return False
    
    def delete_reminder(self, reminder_id: str) -> bool:
        """Delete a reminder"""
        for i, reminder in enumerate(self.reminders):
            if reminder.id == reminder_id:
                del self.reminders[i]
                return True
        return False
    
    def _parse_time_string(self, time_str: str) -> datetime:
        """Parse natural language time strings"""
        now = datetime.now()
        time_str = time_str.lower().strip()
        
        # Handle "in X hours/minutes"
        if time_str.startswith('in '):
            match = re.search(r'in (\d+) (hour|minute)s?', time_str)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                if unit == 'hour':
                    return now + timedelta(hours=amount)
                elif unit == 'minute':
                    return now + timedelta(minutes=amount)
        
        # Handle "tomorrow at X"
        if time_str.startswith('tomorrow'):
            tomorrow = now + timedelta(days=1)
            time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', time_str)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                ampm = time_match.group(3)
                
                if ampm == 'pm' and hour != 12:
                    hour += 12
                elif ampm == 'am' and hour == 12:
                    hour = 0
                
                return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Handle "next X" (day of week)
        day_match = re.search(r'next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)', time_str)
        if day_match:
            day_name = day_match.group(1)
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            target_day = days.index(day_name)
            current_day = now.weekday()
            
            days_ahead = target_day - current_day
            if days_ahead <= 0:
                days_ahead += 7
            
            target_date = now + timedelta(days=days_ahead)
            
            # Extract time if provided
            time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', time_str)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                ampm = time_match.group(3)
                
                if ampm == 'pm' and hour != 12:
                    hour += 12
                elif ampm == 'am' and hour == 12:
                    hour = 0
                
                return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            return target_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Default to 9 AM
        
        # Default: assume it's for today at the specified time
        time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', time_str)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            ampm = time_match.group(3)
            
            if ampm == 'pm' and hour != 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If no time specified, assume 1 hour from now
        return now + timedelta(hours=1)
    
    def get_time(self) -> str:
        """Get current time and date"""
        now = datetime.now()
        return now.strftime("%I:%M %p on %A, %B %d, %Y")
    
    def calculate(self, expression: str) -> str:
        """Simple calculator function"""
        try:
            # Remove common words and keep only mathematical expression
            expression = re.sub(r'\b(what is|calculate|compute|solve|what\'s)\b', '', expression, flags=re.IGNORECASE)
            expression = expression.strip()
            
            # Remove question marks and other punctuation
            expression = re.sub(r'[?.,!]', '', expression)
            
            # Replace words with symbols
            expression = expression.replace('plus', '+')
            expression = expression.replace('minus', '-')
            expression = expression.replace('times', '*')
            expression = expression.replace('multiplied by', '*')
            expression = expression.replace('divided by', '/')
            expression = expression.replace('equals', '=')
            
            # Remove equals sign for evaluation
            expression = expression.replace('=', '')
            
            # Clean up extra spaces
            expression = re.sub(r'\s+', '', expression)
            
            # Validate that we have a mathematical expression
            if not re.search(r'[\+\-\*\/]', expression):
                return "Please provide a mathematical expression with operators like plus, minus, times, or divided by."
            
            # Evaluate the expression
            result = eval(expression)
            return f"The result is {result}"
            
        except Exception as e:
            return f"Sorry, I couldn't calculate that: {str(e)}"
    
    def search_web(self, query: str) -> str:
        """Simulate web search (returns mock results)"""
        return f"I found some information about '{query}'. Here are the top results:\n" \
               f"1. Wikipedia article on {query}\n" \
               f"2. Recent news about {query}\n" \
               f"3. Related research and studies\n" \
               f"Note: This is a simulated search. For real results, you can visit a search engine."
    
    def get_joke(self) -> str:
        """Get a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fish wearing a bowtie? So-fish-ticated!",
            "Why can't you give Elsa a balloon? She will let it go!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus wrecks!"
        ]
        import random
        return random.choice(jokes)
    
    def get_quote(self) -> str:
        """Get an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
        import random
        return random.choice(quotes)

    def get_weather_by_coords(self, lat, lon):
        """Get weather by latitude and longitude using OpenWeatherMap API"""
        try:
            lat = float(lat)
            lon = float(lon)
        except Exception:
            return self.get_weather("New York")
        
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            # Provide realistic mock weather based on coordinates
            # Montreal coordinates: ~45.5017, -73.5673
            if 45.0 <= lat <= 46.0 and -74.0 <= lon <= -73.0:
                # Montreal area
                return WeatherInfo(
                    temperature=22.5,
                    condition="Partly Cloudy",
                    humidity=65,
                    wind_speed=12.0,
                    location="Montreal",
                    forecast=[
                        {"day": "Today", "high": 25, "low": 17, "condition": "Partly Cloudy"},
                        {"day": "Tomorrow", "high": 24, "low": 16, "condition": "Showers"},
                    ]
                )
            return self.get_weather("New York")
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            
            if resp.status_code != 200:
                print(f"Weather API error: {data.get('message', 'Unknown error')}")
                # Fallback to mock data based on coordinates
                if 45.0 <= lat <= 46.0 and -74.0 <= lon <= -73.0:
                    return WeatherInfo(
                        temperature=22.5,
                        condition="Partly Cloudy",
                        humidity=65,
                        wind_speed=12.0,
                        location="Montreal",
                        forecast=[
                            {"day": "Today", "high": 25, "low": 17, "condition": "Partly Cloudy"},
                            {"day": "Tomorrow", "high": 24, "low": 16, "condition": "Showers"},
                        ]
                    )
                return self.get_weather("New York")
            
            if 'main' not in data:
                print(f"Invalid weather API response: {data}")
                return self.get_weather("New York")
            
            temperature = data['main']['temp']
            condition = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            # Get location name, with fallback based on coordinates
            location = data.get('name')
            if not location:
                if 45.0 <= lat <= 46.0 and -74.0 <= lon <= -73.0:
                    location = "Montreal"
                elif 40.0 <= lat <= 41.0 and -74.0 <= lon <= -73.0:
                    location = "New York"
                else:
                    location = f"Location ({lat:.2f}, {lon:.2f})"
            
            forecast = [
                {"day": "Today", "high": temperature, "low": temperature - 10, "condition": condition},
                {"day": "Tomorrow", "high": temperature + 2, "low": temperature - 8, "condition": condition},
            ]
            
            return WeatherInfo(
                temperature=temperature,
                condition=condition,
                humidity=humidity,
                wind_speed=wind_speed,
                location=location,
                forecast=forecast
            )
        except Exception as e:
            print(f"Error in get_weather_by_coords: {e}")
            # Fallback to mock data based on coordinates
            if 45.0 <= lat <= 46.0 and -74.0 <= lon <= -73.0:
                return WeatherInfo(
                    temperature=22.5,
                    condition="Partly Cloudy",
                    humidity=65,
                    wind_speed=12.0,
                    location="Montreal",
                    forecast=[
                        {"day": "Today", "high": 25, "low": 17, "condition": "Partly Cloudy"},
                        {"day": "Tomorrow", "high": 24, "low": 16, "condition": "Showers"},
                    ]
                )
            return self.get_weather("New York")

# Global features instance
prism_features = PrismFeatures() 