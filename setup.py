#!/usr/bin/env python3
"""
Prism AI Voice Assistant Setup Script
This script helps you set up the Prism voice assistant with all necessary configurations.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print the Prism setup banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Prism AI Voice Assistant                  ║
    ║                        Setup Script                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if not env_example.exists():
        print("❌ env_example.txt not found")
        sys.exit(1)
    
    print("\n🔧 Creating .env file...")
    try:
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file and add your API keys")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        sys.exit(1)

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API keys...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = {
        'OPENAI_API_KEY': 'OpenAI API key for GPT-4o',
        'ELEVENLABS_API_KEY': 'ElevenLabs API key for TTS'
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        if not os.getenv(key) or os.getenv(key) == f'your_{key.lower()}_here':
            missing_keys.append(f"{key} ({description})")
    
    if missing_keys:
        print("❌ Missing or default API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease edit the .env file and add your API keys")
        return False
    else:
        print("✅ All API keys are configured")
        return True

def check_google_credentials():
    """Check Google Cloud credentials"""
    print("\n🌐 Checking Google Cloud credentials...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not creds_path or creds_path == 'path/to/your/service-account-key.json':
        print("❌ Google Cloud credentials not configured")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS in your .env file")
        return False
    
    if not os.path.exists(creds_path):
        print(f"❌ Google Cloud credentials file not found: {creds_path}")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        print("✅ Google Cloud credentials file is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading Google Cloud credentials: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing imports...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'flask_socketio',
        'openai',
        'elevenlabs',
        'google.cloud.speech',
        'google.cloud.texttospeech',
        'soundfile',
        'numpy',
        'dotenv'
    ]
    
    failed_imports = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All packages imported successfully")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                        Next Steps                            ║
    ╚══════════════════════════════════════════════════════════════╝
    
    1. 📝 Edit the .env file and add your API keys:
       - OPENAI_API_KEY: Get from https://platform.openai.com/
       - ELEVENLABS_API_KEY: Get from https://elevenlabs.io/
       - GOOGLE_APPLICATION_CREDENTIALS: Path to your Google Cloud service account JSON
    
    2. 🌐 Set up Google Cloud Speech-to-Text API:
       - Go to https://console.cloud.google.com/
       - Create a project or select existing one
       - Enable Speech-to-Text API
       - Create a service account and download JSON key
       - Update GOOGLE_APPLICATION_CREDENTIALS in .env
    
    3. 🚀 Run the application:
       python app.py
    
    4. 🌍 Open your browser and go to:
       http://localhost:5000
    
    For detailed instructions, see README.md
    """)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Check API keys
    api_keys_ok = check_api_keys()
    
    # Check Google credentials
    google_creds_ok = check_google_credentials()
    
    print("\n" + "="*60)
    
    if api_keys_ok and google_creds_ok:
        print("🎉 Setup completed successfully!")
        print("You can now run: python app.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("Please configure the missing items before running the application")
    
    print_next_steps()

if __name__ == "__main__":
    main() 