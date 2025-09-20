#!/usr/bin/env python3
"""
Setup script for AlgoGenie - DSA Problem Solver
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    try:
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Docker is installed")
        
        # Check if Docker daemon is running
        subprocess.check_call(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Docker daemon is running")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running")
        print("Please install Docker Desktop and make sure it's running")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        if "OPENAI_API_KEY" not in content or "your_openai_api_key_here" in content:
            print("❌ Please set your OpenAI API key in the .env file")
            return False
    
    print("✅ .env file is properly configured")
    return True

def main():
    print("🚀 Setting up AlgoGenie - DSA Problem Solver")
    print("=" * 50)
    
    # Check Docker
    if not check_docker():
        print("\n⚠️  Docker is required for code execution. Please install Docker Desktop.")
        return False
    
    # Install requirements
    print("\n📦 Installing requirements...")
    if not install_requirements():
        return False
    
    # Check .env file
    print("\n🔧 Checking configuration...")
    if not check_env_file():
        print("\n📝 Please edit the .env file and add your OpenAI API key:")
        print("   OPENAI_API_KEY=your_actual_api_key_here")
        return False
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 You can now run the application:")
    print("   • For CLI version: python main.py")
    print("   • For web interface: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main()
