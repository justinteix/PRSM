#!/usr/bin/env python3
"""
Prism AI Voice Assistant Test Script
This script tests all components of the Prism voice assistant.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    packages = [
        ('flask', 'Flask web framework'),
        ('flask_cors', 'CORS support'),
        ('flask_socketio', 'WebSocket support'),
        ('openai', 'OpenAI API client'),
        ('elevenlabs', 'ElevenLabs TTS API'),
        ('google.cloud.speech', 'Google Speech API'),
        ('google.cloud.texttospeech', 'Google TTS API'),
        ('soundfile', 'Audio file handling'),
        ('numpy', 'Numerical computing'),
        ('dotenv', 'Environment variables')
    ]
    
    failed = []
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError as e:
            print(f"❌ {package} - {description}: {e}")
            failed.append(package)
    
    return len(failed) == 0

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key',
        'ELEVENLABS_API_KEY': 'ElevenLabs API key'
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value == f'your_{var.lower()}_here':
            print(f"❌ {var} - {description}: Not set")
            missing.append(var)
        else:
            print(f"✅ {var} - {description}: Set")
    
    return len(missing) == 0

def test_google_credentials():
    """Test Google Cloud credentials"""
    print("\n🌐 Testing Google Cloud credentials...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not creds_path or creds_path == 'path/to/your/service-account-key.json':
        print("❌ GOOGLE_APPLICATION_CREDENTIALS: Not configured")
        return False
    
    if not os.path.exists(creds_path):
        print(f"❌ Google Cloud credentials file not found: {creds_path}")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        print("✅ Google Cloud credentials: Valid JSON file")
        return True
    except Exception as e:
        print(f"❌ Google Cloud credentials: Invalid JSON - {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🤖 Testing OpenAI API connection...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai.api_key:
        print("❌ OpenAI API key not set")
        return False
    
    try:
        # Test with a simple request
        from openai import OpenAI
        client = OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using cheaper model
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI API: Connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI API: Connection failed - {e}")
        return False

def test_elevenlabs_connection():
    """Test ElevenLabs API connection"""
    print("\n🎵 Testing ElevenLabs API connection...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    from elevenlabs import voices
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ ElevenLabs API key not set")
        return False
    
    try:
        # Test by getting available voices
        from elevenlabs import voices
        available_voices = voices()
        print(f"✅ ElevenLabs API: Connection successful ({len(available_voices)} voices available)")
        return True
    except Exception as e:
        print(f"❌ ElevenLabs API: Connection failed - {e}")
        return False

def test_google_speech():
    """Test Google Speech API"""
    print("\n🎤 Testing Google Speech API...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    from google.cloud import speech
    
    try:
        client = speech.SpeechClient()
        print("✅ Google Speech API: Client created successfully")
        return True
    except Exception as e:
        print(f"❌ Google Speech API: Client creation failed - {e}")
        return False

def test_flask_app():
    """Test Flask application creation"""
    print("\n🌐 Testing Flask application...")
    
    try:
        from flask import Flask
        from flask_cors import CORS
        from flask_socketio import SocketIO
        
        app = Flask(__name__)
        CORS(app)
        socketio = SocketIO(app, cors_allowed_origins="*")
        
        print("✅ Flask application: Created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask application: Creation failed - {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Prism Test Suite                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Variables", test_environment),
        ("Google Cloud Credentials", test_google_credentials),
        ("OpenAI API", test_openai_connection),
        ("ElevenLabs API", test_elevenlabs_connection),
        ("Google Speech API", test_google_speech),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Test failed with exception - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Results Summary:")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Prism is ready to run.")
        print("Run 'python app.py' to start the application.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        print("See README.md for setup instructions.")

if __name__ == "__main__":
    run_all_tests() 