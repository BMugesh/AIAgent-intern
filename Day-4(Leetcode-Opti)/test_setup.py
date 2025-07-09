#!/usr/bin/env python3
"""
Test script to verify the LeetCode Multi-Agent Optimizer setup
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import autogen
        print("✅ Autogen imported successfully")
    except ImportError as e:
        print(f"❌ Autogen import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True

def test_env_variables():
    """Test if environment variables are properly set"""
    print("\n🔍 Testing environment variables...")
    
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        if groq_api_key == "your_groq_api_key_here":
            print("❌ GROQ_API_KEY is still set to placeholder value")
            print("   Please update your .env file with your actual API key")
            return False
        else:
            print("✅ GROQ_API_KEY is set")
            return True
    else:
        print("❌ GROQ_API_KEY not found")
        print("   Please create a .env file with your Groq API key")
        return False

def test_agents_module():
    """Test if the agents module can be imported and configured"""
    print("\n🔍 Testing agents module...")
    
    try:
        from agents import get_agents, groq_llm_config
        print("✅ Agents module imported successfully")
        
        # Test configuration
        config = groq_llm_config()
        if config and "config_list" in config:
            print("✅ Groq LLM configuration is valid")
        else:
            print("❌ Groq LLM configuration is invalid")
            return False
        
        # Test agent creation
        agents = get_agents()
        if len(agents) == 3:
            print("✅ All three agents created successfully")
            return True
        else:
            print(f"❌ Expected 3 agents, got {len(agents)}")
            return False
            
    except Exception as e:
        print(f"❌ Agents module test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 LeetCode Multi-Agent Optimizer Setup Test\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Variables", test_env_variables),
        ("Agents Module", test_agents_module),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your setup is ready.")
        print("Run 'streamlit run main.py' to start the application.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("Check the README.md for setup instructions.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
