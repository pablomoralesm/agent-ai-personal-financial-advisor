"""Configuration utilities for the Financial Advisor app."""

import os
from typing import Dict, Any

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Database Configuration
DB_CONFIG: Dict[str, Any] = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "financial_advisor")
}

# Google Gemini API
GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")

# Application Settings
DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
