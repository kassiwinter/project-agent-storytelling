"""Core story generation functionality."""

import random
from openai import OpenAI
from ..config.settings import (
    MAX_TOKENS_STORY,
    TEMPERATURE_STORYTELLER
)
from ..config.themes import STORY_THEMES, STORY_MOODS, PEACEFUL_ENDINGS
from ..config.genres import STORY_GENRES
from ..utils.genre_utils import detect_story_genre
from ..utils.llm_utils import call_llm
from ..utils.age_utils import get_age_appropriate_settings

def generate_story(client: OpenAI, user_request: str, age: int) -> str:
    """
    Generates the initial story based on the user's request.
    
    Args:
        client: OpenAI client instance
        user_request: The user's story request
        age: The age of the listener
        
    Returns:
        str: The generated story
    """
    # Detect genre
    story_genre = detect_story_genre(user_request)
    genre_info = STORY_GENRES[story_genre]
    
    # Select random enhancement elements
    theme = random.choice(list(STORY_THEMES.values()))
    mood = random.choice(list(STORY_MOODS.values()))
    ending_style = random.choice(PEACEFUL_ENDINGS)
    
    # Get age-appropriate settings
    age_settings = get_age_appropriate_settings(age)
    
    user_prompt = f"""Create a perfect bedtime story for a {age}-year-old based on:
                        User Idea: \"\"\"
                        {user_request}
                        \"\"\"

    ---
    STORY DETAILS:
    - Genre: {genre_info['name']} - {genre_info['description']}
    - Theme to weave in: {theme}
    - Overall mood: {mood}
    - Ending approach: {ending_style}

    ---
    AGE-SPECIFIC REQUIREMENTS:
    - Target length: {age_settings['length_guide']}
    - Language complexity: {age_settings['language_guide']}
    - Must include: Natural dialogue between characters, sensory details (sights/sounds/feelings), clear story structure

    ---
    BEDTIME STORY ESSENTIALS:
    - Gentle challenge that gets resolved positively
    - Main character a {age}-year-old can relate to
    - Natural lesson about kindness, courage, friendship, or family
    - Peaceful, comforting ending perfect for sleep
    - Rich descriptions that help children visualize scenes
    - Story naturally winds down toward a calm conclusion
    """
    
    from ..prompts.storyteller_prompts import STORYTELLER_SYSTEM_PROMPT
    story = call_llm(
        client=client,
        system_prompt_content=STORYTELLER_SYSTEM_PROMPT,
        user_prompt_content=user_prompt,
        max_tokens=MAX_TOKENS_STORY,
        temperature=TEMPERATURE_STORYTELLER
    )
    return story 