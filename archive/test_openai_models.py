#!/usr/bin/env python3
"""
Test OpenAI Model Access
This script tests which OpenAI models you have access to.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_model_access():
    """Test access to different OpenAI models"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No OpenAI API key found in .env file")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Models to test
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-4o-mini", 
        "gpt-4o",
        "gpt-4",
        "gpt-4-turbo"
    ]
    
    print("🧪 Testing OpenAI Model Access")
    print("=" * 50)
    
    for model in models_to_test:
        try:
            print(f"Testing {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print(f"✅ {model} - Access granted")
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print(f"⚠️  {model} - Quota exceeded (add billing)")
            elif "not found" in error_msg.lower():
                print(f"❌ {model} - Model not available")
            else:
                print(f"❌ {model} - Error: {error_msg[:100]}...")
    
    print("\n" + "=" * 50)
    print("💡 To fix quota issues:")
    print("1. Go to: https://platform.openai.com/account/billing")
    print("2. Add a payment method")
    print("3. You'll get access to all models with pay-as-you-go pricing")

if __name__ == "__main__":
    test_model_access() 