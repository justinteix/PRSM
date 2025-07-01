#!/usr/bin/env python3
"""
Simple test for OpenAI Whisper API
"""

import os
import tempfile
import wave
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_whisper_simple():
    """Test Whisper with a simple audio file"""
    print("🧪 Testing OpenAI Whisper API...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY found")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Create a simple test audio file
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file_path = temp_file.name
                
                # Create a minimal WAV file (1 second of silence)
                with wave.open(temp_file_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz
                    wav_file.writeframes(b'\x00' * 32000)  # 1 second of silence
            
            print(f"📁 Created test audio file: {temp_file_path}")
            
            # Test Whisper transcription
            with open(temp_file_path, 'rb') as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            
            print(f"✅ Whisper transcription successful: '{response.text}'")
            return True
            
        except Exception as e:
            print(f"❌ Whisper error: {e}")
            return False
        finally:
            # Clean up
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    print("🗑️  Cleaned up test file")
                except Exception as e:
                    print(f"⚠️  Could not delete test file: {e}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_whisper_simple()
    if success:
        print("\n🎉 Whisper API is working correctly!")
    else:
        print("\n❌ Whisper API test failed") 