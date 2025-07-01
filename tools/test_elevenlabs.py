#!/usr/bin/env python3
"""
Test ElevenLabs API key and list available voices
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_elevenlabs_api():
    """Test ElevenLabs API key and list voices"""
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key:
        print("❌ No ElevenLabs API key found in .env file")
        return False
    
    print(f"🔑 Testing API key: {api_key[:20]}...")
    
    # Test the API by listing voices
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "xi-api-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ API key is valid! Found {len(voices.get('voices', []))} voices:")
            
            for voice in voices.get('voices', [])[:5]:  # Show first 5 voices
                print(f"  - {voice.get('name', 'Unknown')} (ID: {voice.get('voice_id', 'Unknown')})")
            
            return True
        else:
            print(f"❌ API key is invalid. Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == "__main__":
    test_elevenlabs_api() 