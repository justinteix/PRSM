#!/usr/bin/env python3
"""
Debug script to test audio format handling
"""

import os
import tempfile
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_audio_format():
    """Test different audio formats with Whisper"""
    print("🔍 Testing audio format handling...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OPENAI_API_KEY found")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test with a simple webm file
        print("🧪 Testing with webm format...")
        
        # Create a minimal webm file (this is just a test)
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
            # Write some dummy data (this won't work, but let's see the error)
            temp_file.write(b'fake_webm_data')
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            print("✅ WebM test successful")
        except Exception as e:
            print(f"❌ WebM test failed: {e}")
        finally:
            os.unlink(temp_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_audio_format() 