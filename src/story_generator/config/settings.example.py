"""Configuration settings for the story generator."""

# OpenAI API Configuration
OPENAI_API_KEY = "your-api-key-here"  # Replace with your OpenAI API key
MODEL_NAME = "gpt-3.5-turbo"

# Token Limits
MAX_TOKENS_STORY = 700
MAX_TOKENS_JUDGE = 300

# Temperature Settings
TEMPERATURE_STORYTELLER = 0.8
TEMPERATURE_JUDGE = 0.2
TEMPERATURE_REVISION = 0.6 