#!/usr/bin/env python3
"""
Test script for Google Cloud Speech-to-Text API
"""

import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_speech():
    """Test Google Cloud Speech-to-Text API"""
    try:
        from google.cloud import speech
        
        print("🔍 Testing Google Cloud Speech-to-Text API...")
        
        # Check if credentials are set
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            print("Please set it to the path of your Google Cloud service account key file")
            return False
        
        # Initialize the client
        client = speech.SpeechClient()
        print("✅ Google Cloud Speech client initialized successfully")
        
        # Create a simple test audio file (1 second of silence)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            # Create a simple WAV file with 1 second of silence
            import wave
            import struct
            
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                
                # Create 1 second of silence
                silence = struct.pack('h', 0) * 16000
                wav_file.writeframes(silence)
            
            print(f"✅ Created test audio file: {temp_file.name}")
            
            # Read the audio file
            with open(temp_file.name, 'rb') as audio_file:
                content = audio_file.read()
            
            # Configure the recognition
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
                enable_automatic_punctuation=True,
            )
            
            print("🎤 Sending test audio to Google Cloud Speech-to-Text...")
            response = client.recognize(config=config, audio=audio)
            
            # Check response
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                print(f"✅ API working! Transcript: '{transcript}' (confidence: {confidence:.2f})")
            else:
                print("✅ API working! No speech detected (expected for silence)")
            
            # Clean up
            os.unlink(temp_file.name)
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing Google Cloud Speech-to-Text: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Google Cloud Speech-to-Text API Test")
    print("=" * 60)
    
    success = test_google_speech()
    
    if success:
        print("\n✅ Google Cloud Speech-to-Text API is working correctly!")
        print("You can now use the full Prism app with real speech recognition.")
    else:
        print("\n❌ Google Cloud Speech-to-Text API test failed.")
        print("Please check your Google Cloud credentials and billing setup.") 