#!/usr/bin/env python3
"""
Setup script for Prism AI Voice Assistant Features
Helps users configure optional API keys for enhanced functionality
"""

import os
import requests
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and load it"""
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Found existing .env file")
        return True
    else:
        print("⚠️  No .env file found. Creating one...")
        return False

def get_user_input(prompt, default=""):
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def test_openweather_api(api_key):
    """Test OpenWeather API key"""
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': 'London',
            'appid': api_key,
            'units': 'imperial'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ OpenWeather API key is valid")
            return True
        else:
            print(f"❌ OpenWeather API key test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenWeather API test error: {e}")
        return False

def test_news_api(api_key):
    """Test News API key"""
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': 'us',
            'apiKey': api_key,
            'pageSize': 1
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ News API key is valid")
            return True
        else:
            print(f"❌ News API key test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ News API test error: {e}")
        return False

def setup_optional_apis():
    """Setup optional API keys for enhanced features"""
    print("\n🔧 Setting up Optional API Keys")
    print("=" * 50)
    print("These API keys are optional but provide enhanced functionality:")
    print("- OpenWeather API: Real weather data instead of mock data")
    print("- News API: Real news headlines instead of mock data")
    print()
    
    # Check existing values
    existing_openweather = os.getenv('OPENWEATHER_API_KEY', '')
    existing_news = os.getenv('NEWS_API_KEY', '')
    
    # OpenWeather API setup
    print("🌤️ OpenWeather API Setup")
    print("- Sign up at: https://openweathermap.org/api")
    print("- Get your free API key")
    print("- This provides real weather data")
    print()
    
    openweather_key = get_user_input("Enter your OpenWeather API key (or press Enter to skip)", existing_openweather)
    
    if openweather_key and openweather_key != existing_openweather:
        print("Testing OpenWeather API key...")
        if test_openweather_api(openweather_key):
            os.environ['OPENWEATHER_API_KEY'] = openweather_key
            print("✅ OpenWeather API key saved")
        else:
            print("⚠️  OpenWeather API key test failed. You can still use mock data.")
            openweather_key = ""
    
    # News API setup
    print("\n📰 News API Setup")
    print("- Sign up at: https://newsapi.org/")
    print("- Get your free API key")
    print("- This provides real news headlines")
    print()
    
    news_key = get_user_input("Enter your News API key (or press Enter to skip)", existing_news)
    
    if news_key and news_key != existing_news:
        print("Testing News API key...")
        if test_news_api(news_key):
            os.environ['NEWS_API_KEY'] = news_key
            print("✅ News API key saved")
        else:
            print("⚠️  News API key test failed. You can still use mock data.")
            news_key = ""
    
    return openweather_key, news_key

def update_env_file(openweather_key, news_key):
    """Update or create .env file with new API keys"""
    env_content = []
    
    # Read existing .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('OPENWEATHER_API_KEY='):
                        if openweather_key:
                            env_content.append(f'OPENWEATHER_API_KEY={openweather_key}')
                        else:
                            env_content.append(line)
                    elif line.startswith('NEWS_API_KEY='):
                        if news_key:
                            env_content.append(f'NEWS_API_KEY={news_key}')
                        else:
                            env_content.append(line)
                    else:
                        env_content.append(line)
    
    # Add new keys if they don't exist
    if openweather_key and not any(line.startswith('OPENWEATHER_API_KEY=') for line in env_content):
        env_content.append(f'OPENWEATHER_API_KEY={openweather_key}')
    
    if news_key and not any(line.startswith('NEWS_API_KEY=') for line in env_content):
        env_content.append(f'NEWS_API_KEY={news_key}')
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content))
        f.write('\n')
    
    print("✅ .env file updated")

def show_feature_summary():
    """Show a summary of available features"""
    print("\n🎉 Feature Setup Complete!")
    print("=" * 50)
    print("Your Prism AI Voice Assistant now supports:")
    print()
    print("✅ Core Features (Always Available):")
    print("  - Voice recognition and synthesis")
    print("  - Natural language processing")
    print("  - Time and date information")
    print("  - Calculator functionality")
    print("  - Jokes and quotes")
    print("  - Smart reminders")
    print("  - Web search simulation")
    print()
    
    if os.getenv('OPENWEATHER_API_KEY'):
        print("✅ Enhanced Weather (Real Data):")
        print("  - Live weather conditions")
        print("  - 5-day forecasts")
        print("  - Location-based weather")
    else:
        print("⚠️  Weather (Mock Data):")
        print("  - Sample weather information")
        print("  - Add OPENWEATHER_API_KEY for real data")
    
    if os.getenv('NEWS_API_KEY'):
        print("✅ Enhanced News (Real Data):")
        print("  - Live news headlines")
        print("  - Multiple categories")
        print("  - Recent articles")
    else:
        print("⚠️  News (Mock Data):")
        print("  - Sample news headlines")
        print("  - Add NEWS_API_KEY for real data")
    
    print("\n🚀 Ready to use! Run 'python app.py' to start Prism")

def main():
    """Main setup function"""
    print("🔧 Prism AI Voice Assistant - Feature Setup")
    print("=" * 60)
    print("This script helps you configure optional API keys")
    print("for enhanced weather and news functionality.")
    print()
    
    # Check existing configuration
    check_env_file()
    
    # Setup optional APIs
    openweather_key, news_key = setup_optional_apis()
    
    # Update .env file
    update_env_file(openweather_key, news_key)
    
    # Show summary
    show_feature_summary()

if __name__ == "__main__":
    main() 