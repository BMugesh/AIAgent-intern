#!/usr/bin/env python3
"""
Quick Start Script for LeetCode Multi-Agent Optimizer
Run this to immediately test the system with a sample problem
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print welcome banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🧠 LeetCode Multi-Agent Optimizer - Quick Start          ║
║                                                              ║
║    🔄 Feedback Loop Edition • 5 AI Agents • Enhanced UI     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_requirements():
    """Check if system is ready"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("💡 Please run: python install.py")
        return False
    print("✅ Environment file found")
    
    # Check key packages
    try:
        import streamlit
        import autogen
        print("✅ Required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Please run: python install.py")
        return False
    
    return True

def run_quick_demo():
    """Run a quick demo with a sample problem"""
    print("\n🚀 Starting Quick Demo...")
    print("📝 Using sample problem: Two Sum")
    
    sample_problem = """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists."""
    
    print(f"\n📋 Problem: {sample_problem[:100]}...")
    print("\n🤖 Agents will process this problem:")
    print("   🔧 Code Generator - Generate solution")
    print("   🔍 Code Reviewer - Review code")
    print("   🧪 Test Validator - Run tests")
    print("   🔄 Feedback Coordinator - Handle failures")
    print("   ⚡ Code Optimizer - Optimize solution")
    
    # Test the system
    try:
        from agents import run_leetcode_optimizer
        print("\n⚡ Running multi-agent system...")
        
        # Simulate progress
        for i in range(5):
            print(f"   {'█' * (i+1)}{'░' * (4-i)} {(i+1)*20}%")
            time.sleep(0.5)
        
        result = run_leetcode_optimizer(sample_problem)
        print("\n✅ Quick demo completed successfully!")
        print("🎉 System is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Try running the full application: python run.py")

def launch_full_app():
    """Launch the full Streamlit application"""
    print("\n🚀 Launching full application...")
    print("🌐 Opening browser to http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Failed to launch: {e}")

def main():
    """Main quick start function"""
    print_banner()
    
    if not check_requirements():
        print("\n💡 Setup required. Please run:")
        print("   python install.py")
        return
    
    print("\n🎯 Quick Start Options:")
    print("1. 🏃 Run Quick Demo (test system)")
    print("2. 🚀 Launch Full Application")
    print("3. 📚 Show Documentation")
    print("4. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                run_quick_demo()
                break
            elif choice == "2":
                launch_full_app()
                break
            elif choice == "3":
                show_documentation()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

def show_documentation():
    """Show available documentation"""
    print("\n📚 Available Documentation:")
    print("   📖 README.md - Main documentation")
    print("   🔄 FEEDBACK_LOOP_GUIDE.md - Feedback system guide")
    print("   🎨 UI_SHOWCASE.md - UI enhancement showcase")
    print("   📋 FINAL_SUMMARY.md - Complete system summary")
    
    docs = {
        "README.md": "Main documentation and setup guide",
        "FEEDBACK_LOOP_GUIDE.md": "Comprehensive feedback loop system guide",
        "UI_SHOWCASE.md": "UI enhancement and design showcase",
        "FINAL_SUMMARY.md": "Complete system summary and features"
    }
    
    print("\n📖 Documentation files:")
    for doc, description in docs.items():
        if os.path.exists(doc):
            print(f"   ✅ {doc} - {description}")
        else:
            print(f"   ❌ {doc} - Missing")

if __name__ == "__main__":
    main()
