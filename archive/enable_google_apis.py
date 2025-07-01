#!/usr/bin/env python3
"""
Script to enable Google Cloud APIs for Prism
"""

import os
import webbrowser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def enable_google_apis():
    """Open browser to enable required Google Cloud APIs"""
    
    print("🔧 Google Cloud API Setup Helper")
    print("=" * 50)
    
    # Get project ID from credentials or use default
    project_id = "588116594289"  # From the error message
    
    print(f"Project ID: {project_id}")
    print()
    
    # URLs to enable APIs
    apis = {
        "Speech-to-Text": f"https://console.developers.google.com/apis/api/speech.googleapis.com/overview?project={project_id}",
        "Billing": f"https://console.cloud.google.com/billing?project={project_id}",
        "IAM & Service Accounts": f"https://console.cloud.google.com/iam-admin/serviceaccounts?project={project_id}"
    }
    
    print("📋 Required Setup Steps:")
    print("1. Enable Speech-to-Text API")
    print("2. Verify billing is enabled")
    print("3. Check service account permissions")
    print()
    
    for name, url in apis.items():
        print(f"🌐 Opening {name}...")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"   Manual URL: {url}")
        print()
    
    print("✅ Setup links opened in browser")
    print()
    print("📝 Next steps:")
    print("1. Enable the Speech-to-Text API")
    print("2. Wait 5-10 minutes for changes to propagate")
    print("3. Run: python test_google_speech.py")
    print("4. If successful, run: python app.py")

if __name__ == "__main__":
    enable_google_apis() 