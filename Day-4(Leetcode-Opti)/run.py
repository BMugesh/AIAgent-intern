#!/usr/bin/env python3
"""
Run script for LeetCode Multi-Agent Optimizer
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("Please run: python install.py")
        return False
    
    # Check if required packages are installed
    try:
        import streamlit
        import autogen
        import groq
        from dotenv import load_dotenv
        print("✅ All packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: python install.py")
        return False
    
    # Check if API key is set
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not properly set in .env file")
        print("Please edit .env file and add your actual API key")
        return False
    
    print("✅ All requirements met")
    return True

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting LeetCode Multi-Agent Optimizer...")
    
    try:
        # Run streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
        print("✅ Application started successfully!")
        print("🌐 Opening browser...")
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        print("\n" + "="*50)
        print("🧠 LeetCode Multi-Agent Optimizer is running!")
        print("="*50)
        print("📍 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("="*50)
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        process.terminate()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False
    
    return True

def show_help():
    """Show help information"""
    print("""
🧠 LeetCode Multi-Agent Optimizer - Run Script

Usage:
    python run.py [options]

Options:
    --help, -h     Show this help message
    --check        Only check requirements, don't run
    --install      Run installation first, then start app

Examples:
    python run.py              # Start the application
    python run.py --check      # Check if everything is set up
    python run.py --install    # Install and then run

For more information, see README.md
""")

def main():
    """Main function"""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        show_help()
        return True
    
    if "--install" in args:
        print("🔧 Running installation first...")
        result = subprocess.run([sys.executable, "install.py"])
        if result.returncode != 0:
            print("❌ Installation failed")
            return False
        print("✅ Installation completed")
    
    if "--check" in args:
        return check_requirements()
    
    # Check requirements
    if not check_requirements():
        print("\n💡 Tip: Run 'python run.py --install' to set up everything automatically")
        return False
    
    # Run the application
    return run_streamlit()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
