#!/usr/bin/env python3
"""
Prism AI Voice Assistant - Main Application Entry Point
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from config directory
from dotenv import load_dotenv
load_dotenv('config/.env')

from prism import create_app

def main():
    """Main application entry point"""
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {missing_vars}")
        print("Please set these in your config/.env file")
    
    # Check for Google Cloud credentials
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not set")
        print("Speech-to-text will not work without Google Cloud credentials")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS to your service account key file path")
    
    # Create and run the application
    app, socketio = create_app()
    
    print("🚀 Starting Prism AI Voice Assistant...")
    print("📱 Web interface available at: http://localhost:5000")
    print("🎤 Voice features require Google Cloud Speech-to-Text API")
    print("🤖 AI responses require OpenAI API key")
    print("🌤️  Weather features require OpenWeather API key")
    print("📰 News features require NewsAPI key")
    print("\nPress Ctrl+C to stop the server")
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 