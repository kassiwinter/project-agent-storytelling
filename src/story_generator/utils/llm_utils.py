"""Utilities for interacting with the OpenAI API."""

from openai import OpenAI
from ..config.settings import (
    OPENAI_API_KEY,
    MODEL_NAME
)

def initialize_openai_client():
    """Initialize and return an OpenAI client."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        exit()

def call_llm(client: OpenAI, system_prompt_content: str, user_prompt_content: str, max_tokens: int, temperature: float) -> str:
    """
    Make a call to the OpenAI ChatCompletion API.
    
    Args:
        client: OpenAI client instance
        system_prompt_content: The system prompt to use
        user_prompt_content: The user prompt to use
        max_tokens: Maximum tokens to generate
        temperature: Temperature setting for response creativity
    
    Returns:
        str: The generated response text
    """
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt_content},
                {"role": "user", "content": user_prompt_content}
            ],
            stream=False,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Error: Could not generate response from LLM." 