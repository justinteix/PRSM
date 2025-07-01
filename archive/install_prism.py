#!/usr/bin/env python3
"""
Prism AI Voice Assistant Installation Script
This script provides an alternative installation method with better error handling.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print the Prism installation banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Prism AI Voice Assistant                  ║
    ║                      Installation Script                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n📦 Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Could not upgrade pip, continuing anyway...")
        return True

def install_setuptools():
    """Install/upgrade setuptools"""
    print("\n🔧 Installing setuptools...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel"])
        print("✅ Setuptools installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install setuptools")
        return False

def install_packages_individual():
    """Install packages individually to handle errors better"""
    packages = [
        ("flask", "Flask web framework"),
        ("flask-cors", "CORS support"),
        ("openai", "OpenAI API client"),
        ("elevenlabs", "ElevenLabs TTS API"),
        ("python-dotenv", "Environment variables"),
        ("requests", "HTTP library"),
        ("websockets", "WebSocket support"),
        ("flask-socketio", "Flask SocketIO"),
        ("python-socketio", "Python SocketIO"),
    ]
    
    # Google Cloud packages (these might need special handling)
    google_packages = [
        ("google-cloud-speech", "Google Speech API"),
        ("google-cloud-texttospeech", "Google TTS API"),
    ]
    
    print("\n📦 Installing core packages...")
    failed_packages = []
    
    for package, description in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} - {description}")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} - {description}: Failed")
            failed_packages.append(package)
    
    print("\n🌐 Installing Google Cloud packages...")
    for package, description in google_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} - {description}")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} - {description}: Failed")
            failed_packages.append(package)
    
    return failed_packages

def create_env_file():
    """Create .env file from template"""
    env_file = "env_example.txt"
    target_file = ".env"
    
    if os.path.exists(target_file):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists(env_file):
        print("❌ env_example.txt not found")
        return False
    
    print("\n🔧 Creating .env file...")
    try:
        with open(env_file, 'r') as src, open(target_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file and add your API keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_installation():
    """Test if the installation was successful"""
    print("\n🧪 Testing installation...")
    
    test_packages = [
        'flask',
        'flask_cors',
        'openai',
        'elevenlabs',
        'dotenv',
        'requests',
        'websockets',
        'flask_socketio',
        'socketio'
    ]
    
    failed_imports = []
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
    
    # Test Google Cloud packages separately
    try:
        from google.cloud import speech
        print("✅ google.cloud.speech")
    except ImportError:
        print("❌ google.cloud.speech")
        failed_imports.append("google.cloud.speech")
    
    try:
        from google.cloud import texttospeech
        print("✅ google.cloud.texttospeech")
    except ImportError:
        print("❌ google.cloud.texttospeech")
        failed_imports.append("google.cloud.texttospeech")
    
    return len(failed_imports) == 0, failed_imports

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
       - Follow the instructions in google_cloud_setup.md
    
    3. 🚀 Run the application:
       python app.py
    
    4. 🌍 Open your browser and go to:
       http://localhost:5000
    
    For detailed instructions, see README.md
    """)

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install setuptools
    if not install_setuptools():
        print("❌ Installation failed due to setuptools issue")
        sys.exit(1)
    
    # Install packages individually
    failed_packages = install_packages_individual()
    
    # Create .env file
    create_env_file()
    
    # Test installation
    success, failed_imports = test_installation()
    
    print("\n" + "="*60)
    
    if success:
        print("🎉 Installation completed successfully!")
        print("You can now run: python app.py")
    else:
        print("⚠️  Installation completed with some issues")
        print(f"Failed packages: {', '.join(failed_imports)}")
        print("\nYou can try installing failed packages manually:")
        for package in failed_imports:
            print(f"pip install {package}")
    
    print_next_steps()

if __name__ == "__main__":
    main() 