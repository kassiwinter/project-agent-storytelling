"""Utilities for interacting with language models."""

from openai import OpenAI
from openai.types.chat import ChatCompletion
from ..config.settings import (
    OPENAI_API_KEY,
    MODEL_NAME,
    MAX_TOKENS_STORY,
    TEMPERATURE_STORYTELLER
)

def initialize_openai_client():
    """Initialize and return an OpenAI client."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        exit()

def call_llm(
    client: OpenAI,
    system_prompt_content: str,
    user_prompt_content: str,
    max_tokens: int = MAX_TOKENS_STORY,
    temperature: float = TEMPERATURE_STORYTELLER
) -> str:
    """Call the language model and return its response."""
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt_content},
                {"role": "user", "content": user_prompt_content}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}") 