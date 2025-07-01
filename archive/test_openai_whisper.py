#!/usr/bin/env python3
"""
Test script to verify OpenAI Whisper API access
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_whisper():
    """Test OpenAI Whisper API access"""
    print("🔍 Testing OpenAI Whisper API...")
    
    # Check environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ Found OpenAI API key")
    else:
        print("❌ No OPENAI_API_KEY found")
        return False
    
    # Test Whisper API access
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
        # Create a simple test audio file (silence)
        import tempfile
        import wave
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            # Create a minimal WAV file (1 second of silence)
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                wav_file.writeframes(b'\x00' * 32000)  # 1 second of silence
        
        print("🧪 Testing Whisper with silent audio...")
        
        with open(temp_file.name, 'rb') as audio_file:
            try:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
                print(f"✅ Whisper API working (transcript: '{response.text}')")
                os.unlink(temp_file.name)
                return True
            except Exception as e:
                if "file is too short" in str(e).lower():
                    print("✅ Whisper API working (expected error for silent audio)")
                    os.unlink(temp_file.name)
                    return True
                else:
                    print(f"❌ Whisper API error: {e}")
                    os.unlink(temp_file.name)
                    return False
                    
    except ImportError:
        print("❌ openai package not installed")
        print("   Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        return False

def test_openai_tts():
    """Test OpenAI TTS API access"""
    print("\n🔍 Testing OpenAI TTS API...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        print("🧪 Testing TTS with sample text...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Hello, this is a test of the OpenAI TTS API."
        )
        
        print("✅ TTS API working")
        return True
        
    except Exception as e:
        print(f"❌ TTS API error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing OpenAI APIs for Prism...\n")
    
    whisper_ok = test_openai_whisper()
    tts_ok = test_openai_tts()
    
    if whisper_ok and tts_ok:
        print("\n🎉 All OpenAI APIs are ready!")
        print("   You can now run: python app.py")
    else:
        print("\n📋 Some APIs need attention:")
        if not whisper_ok:
            print("   - Whisper API needs setup")
        if not tts_ok:
            print("   - TTS API needs setup")
        print("\n   Check your OpenAI API key and billing status") 