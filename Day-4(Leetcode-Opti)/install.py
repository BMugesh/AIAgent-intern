#!/usr/bin/env python3
"""
Installation script for LeetCode Multi-Agent Optimizer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.8 or higher")
        return False

def install_requirements():
    """Install required packages"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    return run_command("pip install -r requirements.txt", "Installing requirements")

def setup_environment():
    """Set up environment file"""
    print("🔄 Setting up environment file...")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping environment setup")
            return True
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from template")
        print("📝 Please edit .env file and add your GROQ_API_KEY")
        return True
    else:
        print("❌ .env.example not found")
        return False

def test_installation():
    """Test if installation was successful"""
    print("🔄 Testing installation...")
    
    try:
        # Test imports
        import streamlit
        import autogen
        import groq
        from dotenv import load_dotenv
        print("✅ All packages imported successfully")
        
        # Test configuration
        from config import Config
        print("✅ Configuration loaded successfully")
        
        # Test agents
        from agents import get_agents
        print("✅ Agents module loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 LeetCode Multi-Agent Optimizer Installation")
    print("=" * 50)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Install Requirements", install_requirements),
        ("Setup Environment", setup_environment),
        ("Test Installation", test_installation),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    print("📊 INSTALLATION SUMMARY")
    print("=" * 50)
    
    if not failed_steps:
        print("🎉 Installation completed successfully!")
        print("\n📝 Next steps:")
        print("1. Edit .env file and add your GROQ_API_KEY")
        print("2. Get your API key from: https://console.groq.com/keys")
        print("3. Run: streamlit run main.py")
        print("4. Open your browser to http://localhost:8501")
    else:
        print(f"❌ Installation failed. Failed steps: {', '.join(failed_steps)}")
        print("\n🔧 Troubleshooting:")
        print("- Make sure you have Python 3.8+ installed")
        print("- Check your internet connection")
        print("- Try running: pip install --upgrade pip")
        print("- For help, check the README.md file")
    
    return len(failed_steps) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
