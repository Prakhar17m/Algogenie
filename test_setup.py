#!/usr/bin/env python3
"""
Test script to verify AlgoGenie setup
"""

import sys
import os
import subprocess
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'streamlit',
        'openai',
        'docker',
        'dotenv',
        'autogen_agentchat',
        'autogen_ext'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n🔍 Testing .env file...")
    
    if not os.path.exists('.env'):
        print("  ❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'OPENAI_API_KEY' not in content:
        print("  ❌ OPENAI_API_KEY not found in .env")
        return False
    
    if 'your_openai_api_key_here' in content:
        print("  ⚠️  Please set your actual OpenAI API key in .env")
        return False
    
    print("  ✅ .env file looks good")
    return True

def test_docker():
    """Test if Docker is available"""
    print("\n🔍 Testing Docker...")
    
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"  ✅ Docker: {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ Docker error: {result.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        print("  ❌ Docker not available")
        return False

def test_project_structure():
    """Test if project structure is correct"""
    print("\n🔍 Testing project structure...")
    
    required_files = [
        'main.py',
        'app.py',
        'requirements.txt',
        'config/settings.py',
        'config/constant.py',
        'team/dsa_team.py',
        'agents/problem_solver.py',
        'agents/code_executor_agent.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_config_imports():
    """Test if project modules can be imported"""
    print("\n🔍 Testing project module imports...")
    
    try:
        from config.settings import get_model_client
        print("  ✅ config.settings")
    except Exception as e:
        print(f"  ❌ config.settings: {e}")
        return False
    
    try:
        from team.dsa_team import get_dsa_team_and_docker
        print("  ✅ team.dsa_team")
    except Exception as e:
        print(f"  ❌ team.dsa_team: {e}")
        return False
    
    return True

def main():
    print("🧪 AlgoGenie Setup Test")
    print("=" * 40)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Imports", test_imports),
        ("Project Module Imports", test_config_imports),
        ("Environment File", test_env_file),
        ("Docker", test_docker)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nYou can now run:")
        print("  • Web interface: streamlit run app.py")
        print("  • CLI interface: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  • Install missing packages: pip install -r requirements.txt")
        print("  • Set your OpenAI API key in .env file")
        print("  • Install and start Docker Desktop")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
