#!/usr/bin/env python3
"""
Simple voice test - create a basic audio file and test with Whisper
"""

import os
import tempfile
import wave
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_test_audio():
    """Create a simple test audio file"""
    print("🎵 Creating test audio file...")
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        # Create a simple WAV file with a tone
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(16000)  # 16kHz
            
            # Create a simple tone (1 second)
            import struct
            samples = []
            for i in range(16000):  # 1 second at 16kHz
                # Simple sine wave at 440Hz
                sample = int(32767 * 0.1 * (i * 440 / 16000))
                samples.append(struct.pack('h', sample))
            
            wav_file.writeframes(b''.join(samples))
        
        print(f"✅ Created test audio: {temp_file.name}")
        return temp_file.name

def test_whisper_with_file(file_path):
    """Test Whisper with the given file"""
    print("🎤 Testing Whisper...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY found")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        with open(file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        
        print(f"✅ Whisper response: '{response.text}'")
        return True
        
    except Exception as e:
        print(f"❌ Whisper error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Voice Test\n")
    
    # Create test audio
    audio_file = create_test_audio()
    
    try:
        # Test with Whisper
        success = test_whisper_with_file(audio_file)
        
        if success:
            print("\n🎉 Voice test successful!")
            print("   The issue might be with browser audio format")
        else:
            print("\n❌ Voice test failed")
            print("   Check your OpenAI API key and billing")
            
    finally:
        # Clean up
        if os.path.exists(audio_file):
            os.unlink(audio_file)
            print("🗑️  Cleaned up test file") 