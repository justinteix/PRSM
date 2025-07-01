#!/usr/bin/env python3
"""
Test script for Prism AI Voice Assistant Features
Tests all the new home assistant capabilities
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_api_endpoint(endpoint, method="GET", data=None, params=None):
    """Test an API endpoint and return the response"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == "PUT":
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        
        print(f"✅ {method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def test_chat_functionality():
    """Test the chat functionality with various feature requests"""
    print("\n🧪 Testing Chat Functionality")
    print("=" * 50)
    
    test_messages = [
        "What's the weather like?",
        "What time is it?",
        "Tell me a joke",
        "What is 15 plus 27?",
        "Give me an inspirational quote",
        "What's the latest news?"
    ]
    
    for message in test_messages:
        print(f"\n📝 Testing: '{message}'")
        success = test_api_endpoint("/api/chat", method="POST", data={"message": message})
        if success:
            print("   ✅ Chat response received")
        else:
            print("   ❌ Chat failed")

def test_weather_api():
    """Test weather API endpoints"""
    print("\n🌤️ Testing Weather API")
    print("=" * 50)
    
    # Test weather with default location
    test_api_endpoint("/api/weather")
    
    # Test weather with specific location
    test_api_endpoint("/api/weather", params={"location": "New York"})

def test_news_api():
    """Test news API endpoints"""
    print("\n📰 Testing News API")
    print("=" * 50)
    
    # Test general news
    test_api_endpoint("/api/news")
    
    # Test technology news
    test_api_endpoint("/api/news", params={"category": "technology", "limit": 3})

def test_time_api():
    """Test time API endpoint"""
    print("\n🕐 Testing Time API")
    print("=" * 50)
    
    test_api_endpoint("/api/time")

def test_calculator_api():
    """Test calculator API endpoint"""
    print("\n🧮 Testing Calculator API")
    print("=" * 50)
    
    test_expressions = [
        "15 + 27",
        "100 / 4",
        "7 * 8",
        "50 - 12"
    ]
    
    for expr in test_expressions:
        print(f"\n📝 Testing: '{expr}'")
        test_api_endpoint("/api/calculate", method="POST", data={"expression": expr})

def test_entertainment_apis():
    """Test entertainment API endpoints"""
    print("\n😄 Testing Entertainment APIs")
    print("=" * 50)
    
    # Test joke API
    test_api_endpoint("/api/joke")
    
    # Test quote API
    test_api_endpoint("/api/quote")

def test_reminder_apis():
    """Test reminder management APIs"""
    print("\n⏰ Testing Reminder APIs")
    print("=" * 50)
    
    # Get all reminders
    test_api_endpoint("/api/reminders")
    
    # Create a new reminder
    reminder_data = {
        "title": "Test reminder",
        "time": "in 1 hour"
    }
    test_api_endpoint("/api/reminders", method="POST", data=reminder_data)
    
    # Get reminders again to see the new one
    test_api_endpoint("/api/reminders")
    
    # Test completing a reminder (this would need a valid reminder ID)
    # test_api_endpoint("/api/reminders", method="PUT", data={"id": "reminder_1", "action": "complete"})

def test_text_to_speech():
    """Test text-to-speech API"""
    print("\n🔊 Testing Text-to-Speech API")
    print("=" * 50)
    
    test_text = "Hello! This is a test of the text-to-speech functionality."
    test_api_endpoint("/api/text-to-speech", method="POST", data={"text": test_text})

def main():
    """Run all feature tests"""
    print("🚀 Prism AI Voice Assistant - Feature Tests")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test all features
    test_chat_functionality()
    test_weather_api()
    test_news_api()
    test_time_api()
    test_calculator_api()
    test_entertainment_apis()
    test_reminder_apis()
    test_text_to_speech()
    
    print("\n" + "=" * 60)
    print("🎉 Feature testing completed!")
    print("\nTo test voice functionality:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Click on the feature cards to try different commands")
    print("3. Use voice mode by clicking and holding the microphone button")

if __name__ == "__main__":
    main() 