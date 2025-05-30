"""Core story judging functionality."""

from openai import OpenAI
from ..config.settings import (
    MAX_TOKENS_JUDGE,
    TEMPERATURE_JUDGE
)
from ..utils.llm_utils import call_llm
from ..utils.age_utils import get_age_appropriate_settings
from ..prompts.judge_prompts import JUDGE_SYSTEM_PROMPT

def judge_story(client: OpenAI, story_text: str, user_request: str, age: int) -> str:
    """
    Judges the story and provides feedback or approval.
    
    Args:
        client: OpenAI client instance
        story_text: The story to judge
        user_request: The original user request
        age: The age of the listener
        
    Returns:
        str: The judgment result
    """
    print("\n Barnaby the Bookworm is carefully reading the story...")

    # Get age-appropriate settings
    age_settings = get_age_appropriate_settings(age)

    user_prompt = f"""
        Review this bedtime story for a {age}-year-old child using expert bedtime story criteria.

        USER'S ORIGINAL REQUEST: '{user_request}'
        TARGET AGE: {age} years old

        STORY TO EVALUATE:
        ---
        {story_text}
        ---

        EVALUATION CRITERIA:

        1. LENGTH & AGE APPROPRIATENESS: Expected {age_settings['length_guide']}
        - Is the word count appropriate for this age?
        - Is the {age_settings['complexity']} suitable?

        2. BEDTIME EMOTIONAL TONE (Most Critical):
        - Engaging but calming (not overstimulating before sleep)
        - Positive, confidence-building messages  
        - Peaceful conclusion that prepares mind for sleep
        - No scary/anxiety-inducing content

        3. STORY QUALITY & STRUCTURE:
        - Clear beginning, middle (gentle challenge), satisfying end
        - Relatable main character for a {age}-year-old
        - Includes natural dialogue and sensory details
        - Good pacing that flows toward calm ending

        4. CHARACTER DEVELOPMENT & LESSONS:
        - Characters show growth, kindness, or problem-solving
        - Natural moral lessons (not preachy)
        - Builds empathy and positive values

        5. BEDTIME SUITABILITY:
        - Story winds down naturally to peaceful conclusion
        - Comforting themes that ease bedtime concerns
        - Language naturally slows toward end

        6. REQUEST FULFILLMENT:
        - Addresses what user asked for creatively
        - Stays true to core idea while being bedtime-appropriate

        RESPONSE FORMAT:
        If story is EXCELLENT for a {age}-year-old's bedtime, respond only:
        STORY_APPROVED

        If needs improvement, respond exactly:
        STORY_NEEDS_REVISION
        [Provide 1-3 sentences with specific, actionable feedback. Focus on the most important changes for bedtime suitability and age-appropriateness.]

        Evaluate now:"""

    judgment = call_llm(
        client=client,
        system_prompt_content=JUDGE_SYSTEM_PROMPT,
        user_prompt_content=user_prompt,
        max_tokens=MAX_TOKENS_JUDGE,
        temperature=TEMPERATURE_JUDGE
    )
    return judgment 