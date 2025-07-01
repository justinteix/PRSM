"""
Core Prism Assistant class
Handles conversation and feature integration
"""

import re
from typing import Dict, List, Optional
from openai import OpenAI
import os

from ..features.weather import weather_service
from ..features.news import news_service
from ..features.reminders import reminder_service
from ..features.calculator import calculator_service
from ..features.jokes import joke_service
from ..features.quotes import quote_service
from ..features.search import search_service

class PrismAssistant:
    """Main assistant class for Prism AI Voice Assistant"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are Prism, an intelligent and helpful AI voice assistant. 
        You should be conversational, friendly, and provide helpful responses. 
        Keep your responses concise but informative. You can help with:
        - General questions and information
        - Weather updates
        - Setting reminders
        - Playing music
        - Controlling smart home devices
        - Providing news updates
        - Answering questions about various topics
        
        Always respond in a natural, conversational tone."""
    
    def process_query(self, user_input: str, lat=None, lon=None) -> str:
        """Process user input and generate response using GPT-4o with integrated features"""
        try:
            # Check for specific feature requests first
            feature_response = self._handle_feature_requests(user_input, lat=lat, lon=lon)
            if feature_response:
                return feature_response
            
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history[-10:]  # Keep last 10 messages
            
            # Get response from GPT-4o
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o-mini for best balance of capability and cost
                messages=messages,  # type: ignore
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            if assistant_response is None:
                assistant_response = "I'm sorry, I couldn't generate a response. Please try again."
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    def _handle_feature_requests(self, user_input: str, lat=None, lon=None) -> Optional[str]:
        """Handle specific feature requests before sending to GPT"""
        user_input_lower = user_input.lower()
        
        # Weather requests
        if any(word in user_input_lower for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cold', 'hot']):
            if lat and lon:
                weather = weather_service.get_weather_by_coords(lat, lon)
            else:
                location = self._extract_location(user_input)
                weather = weather_service.get_weather(location)
            return f"The weather in {weather.location} is currently {weather.temperature} degrees Fahrenheit with {weather.condition}. Humidity is {weather.humidity} percent with wind speed of {weather.wind_speed} miles per hour."
        
        # Time requests
        elif any(word in user_input_lower for word in ['time', 'date', 'what time', 'current time']):
            from datetime import datetime
            now = datetime.now()
            # Format time without leading zeros for better TTS pronunciation
            hour = now.strftime("%I").lstrip("0")  # Remove leading zero from hour
            minute = now.strftime("%M")
            ampm = now.strftime("%p")
            day = now.strftime("%A")
            month = now.strftime("%B")
            day_num = now.strftime("%d").lstrip("0")  # Remove leading zero from day
            year = now.strftime("%Y")
            
            current_time = f"{hour}:{minute} {ampm} on {day}, {month} {day_num}, {year}"
            return f"The current time is {current_time}."
        
        # News requests
        elif any(word in user_input_lower for word in ['news', 'headlines', 'latest news', 'what\'s happening']):
            news_items = news_service.get_news(limit=3)
            if not news_items:
                return "I'm sorry, I couldn't fetch the latest news at the moment."
            
            response = "Here are the latest headlines: "
            for i, item in enumerate(news_items, 1):
                if i == 1:
                    response += f"First, {item.title}. "
                elif i == len(news_items):
                    response += f"Finally, {item.title}."
                else:
                    response += f"Next, {item.title}. "
            return response
        
        # Reminder requests
        elif any(word in user_input_lower for word in ['remind', 'reminder', 'set reminder', 'remind me']):
            return self._handle_reminder_request(user_input)
        
        # Calculator requests
        elif any(word in user_input_lower for word in ['calculate', 'what is', 'plus', 'minus', 'times', 'divided by']):
            result = calculator_service.calculate(user_input)
            # Check if it's a successful calculation (not an error message)
            if not result.startswith("Error") and not result.startswith("I can only"):
                return f"The answer is {result}."
            else:
                return result
        
        # Joke requests
        elif any(word in user_input_lower for word in ['joke', 'funny', 'humor', 'make me laugh']):
            return f"Here's a joke for you: {joke_service.get_joke()}"
        
        # Quote requests
        elif any(word in user_input_lower for word in ['quote', 'inspiration', 'motivation', 'inspirational']):
            return f"Here's an inspirational quote: {quote_service.get_quote()}"
        
        # Search requests
        elif any(word in user_input_lower for word in ['search', 'find', 'look up', 'what is']):
            query = self._extract_search_query(user_input)
            return search_service.search_web(query)
        
        return None  # Let GPT handle it
    
    def _extract_location(self, user_input: str) -> str:
        """Extract location from user input"""
        # Simple location extraction - can be improved
        words = user_input.split()
        location_keywords = ['in', 'at', 'for']
        
        for i, word in enumerate(words):
            if word.lower() in location_keywords and i + 1 < len(words):
                return ' '.join(words[i + 1:])
        
        return "auto"  # Default to auto-detect
    
    def _extract_search_query(self, user_input: str) -> str:
        """Extract search query from user input"""
        # Remove common search words
        query = re.sub(r'\b(search|find|look up|what is|tell me about)\b', '', user_input, flags=re.IGNORECASE)
        return query.strip()
    
    def _handle_reminder_request(self, user_input: str) -> str:
        """Handle reminder creation requests"""
        try:
            # Extract reminder details
            # Look for patterns like "remind me to [task] [time]"
            reminder_match = re.search(r'remind me to (.+?)(?: at | in | on | tomorrow|next)', user_input, re.IGNORECASE)
            if reminder_match:
                title = reminder_match.group(1).strip()
                time_part = user_input[reminder_match.end():].strip()
                
                if time_part:
                    reminder = reminder_service.add_reminder(title, time_part)
                    # Format reminder time without leading zeros for better TTS pronunciation
                    hour = reminder.datetime.strftime("%I").lstrip("0")  # Remove leading zero from hour
                    minute = reminder.datetime.strftime("%M")
                    ampm = reminder.datetime.strftime("%p")
                    day = reminder.datetime.strftime("%A")
                    month = reminder.datetime.strftime("%B")
                    day_num = reminder.datetime.strftime("%d").lstrip("0")  # Remove leading zero from day
                    
                    reminder_time = f"{hour}:{minute} {ampm} on {day}, {month} {day_num}"
                    return f"I've set a reminder for '{title}' at {reminder_time}."
                else:
                    return "Please specify when you'd like to be reminded. For example: 'remind me to call mom tomorrow at 3pm'"
            else:
                return "I didn't understand the reminder format. Please say something like 'remind me to call mom tomorrow at 3pm'"
        except Exception as e:
            return f"Sorry, I couldn't set that reminder: {str(e)}" 