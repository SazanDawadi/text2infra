# config.py
import os
from typing import Optional

def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from environment variables or config file"""
    # Check environment variables first
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        # Fallback to config file
        try:
            with open(".gemini_config", "r") as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            return None
    
    return api_key