#!/usr/bin/env python3
"""
Test OpenRouter API integration
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

async def test_openrouter_api():
    """Test OpenRouter API"""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ No OpenRouter API key found in .env file")
        print("💡 Get your API key from: https://openrouter.ai/keys")
        return False
    
    if api_key == "your_openrouter_api_key_here":
        print("❌ Please set your actual OpenRouter API key in .env file")
        print("💡 Get your API key from: https://openrouter.ai/keys")
        return False
    
    try:
        # Test with OpenRouter
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Test with a free model
        response = await client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[{"role": "user", "content": "Hello! Can you help me with a simple math problem?"}],
            max_tokens=50
        )
        
        print("✅ OpenRouter API is working!")
        print(f"✅ Model: meta-llama/llama-3.1-8b-instruct:free")
        print(f"✅ Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
            print("❌ API quota exceeded or insufficient credits")
            print("💡 Solutions:")
            print("   1. Check your OpenRouter account balance")
            print("   2. Use a free model like 'meta-llama/llama-3.1-8b-instruct:free'")
            print("   3. Add credits to your OpenRouter account")
        elif "invalid" in error_msg.lower() or "unauthorized" in error_msg.lower():
            print("❌ Invalid API key")
            print("💡 Solutions:")
            print("   1. Generate a new API key at: https://openrouter.ai/keys")
            print("   2. Update the .env file with the new key")
        elif "model" in error_msg.lower():
            print("❌ Model not available")
            print("💡 Try a different model in config/constant.py")
            print("   Available free models:")
            print("   - meta-llama/llama-3.1-8b-instruct:free")
            print("   - microsoft/phi-3-medium-128k-instruct:free")
        else:
            print(f"❌ API error: {e}")
        
        return False

async def main():
    print("🔍 Testing OpenRouter API")
    print("=" * 30)
    
    success = await test_openrouter_api()
    
    if success:
        print("\n🎉 OpenRouter integration is ready!")
        print("You can now run:")
        print("  • CLI version: python main.py")
        print("  • Web interface: python -m streamlit run app.py")
    else:
        print("\n🛠️  To fix the issues:")
        print("1. Get API key from: https://openrouter.ai/keys")
        print("2. Update .env file with your key")
        print("3. Run this test again")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
