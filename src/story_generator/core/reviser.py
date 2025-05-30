"""Core story revision functionality."""

import random
from openai import OpenAI
from ..config.settings import (
    MAX_TOKENS_STORY,
    TEMPERATURE_REVISION
)
from ..config.themes import PEACEFUL_ENDINGS
from ..utils.llm_utils import call_llm
from ..utils.age_utils import get_age_appropriate_settings
from ..prompts.storyteller_prompts import STORYTELLER_SYSTEM_PROMPT

def revise_story(client: OpenAI, original_story: str, user_request: str, judge_feedback: str, age: int) -> str:
    """
    Enhanced revision with age-aware guidance and theme consistency.
    
    Args:
        client: OpenAI client instance
        original_story: The original story to revise
        user_request: The original user request
        judge_feedback: Feedback from the judge
        age: The age of the listener
        
    Returns:
        str: The revised story
    """
    print(f"\n🔧 Kassi is polishing the story for the perfect {age}-year-old bedtime experience...")
    
    # Clean up feedback
    if judge_feedback.startswith("STORY_NEEDS_REVISION"):
        actual_feedback = judge_feedback.replace("STORY_NEEDS_REVISION\n", "", 1).strip()
    else:
        actual_feedback = judge_feedback
    
    # Get age-appropriate settings
    age_settings = get_age_appropriate_settings(age)
    
    # Add a peaceful ending reminder
    peaceful_ending = random.choice(PEACEFUL_ENDINGS)

    user_prompt = f"""
    Revise this bedtime story for a {age}-year-old, incorporating the expert feedback.

    USER'S ORIGINAL REQUEST: '{user_request}'
    TARGET AGE: {age} years old - focus on {age_settings['complexity']}

    ORIGINAL STORY:
    ---
    {original_story}
    ---

    EXPERT FEEDBACK TO ADDRESS:
    ---
    {actual_feedback}
    ---

    REVISION REQUIREMENTS:
    - Address ALL the feedback points specifically
    - Maintain the story's heart and appeal
    - Perfect bedtime tone: engaging but calming for peaceful sleep
    - Age-appropriate language and length for {age}-year-old
    - Include natural dialogue and sensory details that bring story to life
    - Ensure peaceful, comforting ending: {peaceful_ending}
    - Natural moral lesson that emerges from the story
    - Story should naturally wind down toward a calm, sleepy conclusion"""
    
    revised_story = call_llm(
        client=client,
        system_prompt_content=STORYTELLER_SYSTEM_PROMPT,
        user_prompt_content=user_prompt,
        max_tokens=MAX_TOKENS_STORY,
        temperature=TEMPERATURE_REVISION
    )
    return revised_story 