"""
Google Gemini AI configuration.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


@dataclass
class GeminiConfig:
    """Configuration class for Google Gemini AI."""
    
    api_key: str
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_output_tokens: int = 2048
    
    @classmethod
    def from_env(cls) -> 'GeminiConfig':
        """Create GeminiConfig from environment variables."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            model_name=os.getenv('GEMINI_MODEL', 'gemini-1.5-flash'),
            temperature=float(os.getenv('GEMINI_TEMPERATURE', '0.7')),
            max_output_tokens=int(os.getenv('GEMINI_MAX_TOKENS', '2048'))
        )
    
    def configure_genai(self) -> None:
        """Configure the Google GenerativeAI library."""
        genai.configure(api_key=self.api_key)
    
    def get_generation_config(self) -> Dict[str, Any]:
        """Get generation configuration for Gemini model."""
        return {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
        }
    
    def __repr__(self) -> str:
        """String representation hiding API key."""
        return (f"GeminiConfig(api_key='***', model_name='{self.model_name}', "
                f"temperature={self.temperature}, max_output_tokens={self.max_output_tokens})")


# Global Gemini configuration instance
try:
    gemini_config = GeminiConfig.from_env()
    gemini_config.configure_genai()
except ValueError as e:
    print(f"Warning: {e}")
    gemini_config = None
