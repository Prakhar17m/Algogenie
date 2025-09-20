#!/usr/bin/env python3
"""
AlgoGenie Launcher - Choose your interface
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Print the AlgoGenie banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🧠 AlgoGenie - AI DSA Problem Solver                     ║
    ║                                                              ║
    ║    ✨ Enhanced with OpenRouter AI                            ║
    ║    🚀 Multiple Interface Options                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import asyncio
        from team.dsa_team import get_dsa_team_and_docker
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_config():
    """Check if configuration is set up"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please create .env file with your OpenRouter API key")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_openrouter_api_key_here" in content:
            print("❌ Please set your actual OpenRouter API key in .env file")
            return False
    
    print("✅ Configuration looks good")
    return True

def launch_interface(choice):
    """Launch the selected interface"""
    if choice == "1":
        print("🚀 Launching Enhanced Dashboard...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_dashboard.py"])
    elif choice == "2":
        print("🚀 Launching Enhanced Web Interface...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_enhanced.py"])
    elif choice == "3":
        print("🚀 Launching Original Web Interface...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    elif choice == "4":
        print("🚀 Launching CLI Interface...")
        subprocess.run([sys.executable, "main.py"])
    elif choice == "5":
        print("🚀 Launching Demo Mode...")
        subprocess.run([sys.executable, "demo_mode.py"])
    elif choice == "6":
        print("🧪 Running Setup Test...")
        subprocess.run([sys.executable, "test_setup.py"])
    elif choice == "7":
        print("🔍 Testing OpenRouter API...")
        subprocess.run([sys.executable, "test_openrouter.py"])

def main():
    print_banner()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check configuration
    if not check_config():
        print("\n💡 Get your OpenRouter API key from: https://openrouter.ai/keys")
        return
    
    print("\n🎯 Choose your interface:")
    print("1. 🎨 Enhanced Dashboard (Recommended)")
    print("2. 🌟 Enhanced Web Interface")
    print("3. 📱 Original Web Interface")
    print("4. 💻 CLI Interface")
    print("5. 🎮 Demo Mode (No API required)")
    print("6. 🧪 Setup Test")
    print("7. 🔍 API Test")
    print("0. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
            launch_interface(choice)
            break
        else:
            print("❌ Invalid choice. Please enter 0-7.")

if __name__ == "__main__":
    main()
