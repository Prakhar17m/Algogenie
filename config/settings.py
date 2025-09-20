import os
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai._model_info import ModelInfo
from config.constant import MODEL

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

def get_model_client():
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found in environment variables. "
            "Please set your OpenRouter API key in the .env file."
        )
    
    try:
        # Define model info for OpenRouter models
        model_info = ModelInfo(
            model_name=MODEL,
            max_tokens=4096,
            context_length=8192,
            supports_tools=False,
            supports_vision=False,
            supports_function_calling=False,
            vision=False,  # Required field
            function_calling=False,  # Required field
            json_output=False,  # Required field
            family="openrouter"  # Required field
        )
        
        # Use OpenRouter's OpenAI-compatible API endpoint
        model_client = OpenAIChatCompletionClient(
            model=MODEL, 
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model_info=model_info
        )
        return model_client
    except Exception as e:
        raise RuntimeError(f"Failed to create OpenRouter client: {e}")


