"""Configuration for the LLM Council."""

import os
import json
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers
# Can be overridden via COUNCIL_MODELS env var as JSON array
# Updated to latest flagship models as of November 2025
_DEFAULT_COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "anthropic/claude-sonnet-4.5",
    "google/gemini-3-pro-preview",
    "x-ai/grok-4.1-fast",
]

def _parse_models_env(env_var: str, default: list) -> list:
    """Parse models from environment variable (JSON array) or use default."""
    env_value = os.getenv(env_var)
    if env_value:
        try:
            models = json.loads(env_value)
            if isinstance(models, list) and all(isinstance(m, str) for m in models):
                return models
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {env_var}, using defaults")
    return default

COUNCIL_MODELS = _parse_models_env("COUNCIL_MODELS", _DEFAULT_COUNCIL_MODELS)

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", "anthropic/claude-sonnet-4.5")

# OpenRouter API endpoint
OPENROUTER_API_URL = os.getenv(
    "OPENROUTER_API_URL",
    "https://openrouter.ai/api/v1/chat/completions"
)

# Data directory for conversation storage
DATA_DIR = os.getenv("DATA_DIR", "data/conversations")

# API settings
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "120"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))

# Server settings
# Heroku uses PORT env var, fallback to SERVER_PORT for local development
SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "8001")))

# CORS origins - allow all in production (same domain), specific origins in development
# In production, frontend is served from the same domain, so CORS is less restrictive
_cors_origins_env = os.getenv("CORS_ORIGINS")
if _cors_origins_env:
    CORS_ORIGINS = json.loads(_cors_origins_env)
elif os.getenv("PYTHON_ENV") == "production" or os.getenv("NODE_ENV") == "production":
    # In production, allow all origins (frontend is on same domain)
    # FastAPI requires explicit list, so we'll handle "*" in main.py
    CORS_ORIGINS = ["*"]
else:
    # Development defaults
    CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
