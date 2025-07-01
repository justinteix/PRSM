#!/usr/bin/env python3
"""
Quick test to check if Google Cloud Speech-to-Text API is enabled
"""

import os
import time

def test_api_status():
    """Test if the API is now enabled"""
    print("🔍 Testing Google Cloud Speech-to-Text API status...")
    print(f"Credentials path: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'Not set')}")
    
    try:
        from google.cloud import speech
        client = speech.SpeechClient()
        print("✅ Client initialized successfully")
        
        # Try a simple test with minimal audio
        import tempfile
        import wave
        import struct
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            # Create a very short WAV file (0.1 seconds of silence)
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                silence = struct.pack('h', 0) * 1600  # 0.1 seconds
                wav_file.writeframes(silence)
            
            with open(temp_file.name, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            
            print("🎤 Testing API call...")
            response = client.recognize(config=config, audio=audio)
            
            if response.results:
                print("✅ API is working! Speech detected.")
            else:
                print("✅ API is working! No speech detected (expected for silence).")
            
            os.unlink(temp_file.name)
            
    except Exception as e:
        error_msg = str(e)
        if "SERVICE_DISABLED" in error_msg:
            print("❌ API is still disabled. Please enable it in the Google Cloud Console.")
            print("   URL: https://console.developers.google.com/apis/api/speech.googleapis.com/overview?project=588116594289")
        elif "403" in error_msg:
            print("❌ Permission denied. Check your service account permissions.")
        else:
            print(f"❌ Error: {error_msg}")

if __name__ == "__main__":
    test_api_status() 