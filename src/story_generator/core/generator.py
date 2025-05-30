"""Story generation agent."""

from typing import Dict, Optional, Tuple
from openai import OpenAI
from ..utils.llm_utils import call_llm
from ..config.content_filter import FORBIDDEN_TOPICS, AGE_GUIDELINES, POSITIVE_THEMES

GENERATION_PROMPT = """You are an expert children's story writer. Create an engaging, age-appropriate bedtime story.

IMPORTANT: This story MUST be appropriate for children. DO NOT include:
- Any references to drugs, alcohol, or smoking
- Violence or scary content
- Adult relationships or romance
- Inappropriate behavior like bullying or lying
- Any content that could be traumatic or anxiety-inducing

USER REQUEST: {request}
TARGET AGE: {age}
AGE GUIDELINES: {age_guidelines}
STORY PLAN: {plan}

If provided, incorporate this feedback for improvement:
{feedback}

Create a story that:
1. Is engaging but calming (suitable for bedtime)
2. Has clear character development
3. Includes gentle life lessons
4. Uses age-appropriate language
5. Has a satisfying, peaceful ending
6. Focuses on positive themes like: {positive_themes}

The story should be approximately {length} words."""

class StoryGenerator:
    def __init__(self, client: OpenAI):
        self.client = client

    def _contains_forbidden_content(self, text: str) -> Tuple[bool, str]:
        """Check if text contains any forbidden topics."""
        text = text.lower()
        for topic, info in FORBIDDEN_TOPICS.items():
            for keyword in info["keywords"]:
                if keyword.lower() in text:
                    return True, f"Content warning: {info['reason']} (found: {keyword})"
        return False, ""

    def _is_age_appropriate(self, text: str, age: int) -> Tuple[bool, str]:
        """Check if content is age-appropriate."""
        # Basic length check (younger kids need shorter stories)
        word_count = len(text.split())
        max_words = {
            5: 500,
            6: 600,
            7: 700,
            8: 800,
            9: 900,
            10: 1000
        }
        if word_count > max_words.get(age, 800):
            return False, f"Story is too long for age {age} ({word_count} words)"
        
        # Check for complex language in young children's stories
        if age <= 7:
            complex_words = [word for word in text.split() if len(word) > 8]
            if len(complex_words) > word_count * 0.05:  # More than 5% complex words
                return False, f"Language may be too complex for age {age}"
        
        return True, ""

    def generate_story(
        self, 
        request: str, 
        age: int, 
        plan: Dict,
        feedback: Optional[list] = None,
        target_length: int = 500
    ) -> str:
        """Generate or regenerate a story based on request and optional feedback."""
        # First, check if the request itself contains inappropriate content
        has_forbidden, forbidden_msg = self._contains_forbidden_content(request)
        if has_forbidden:
            safe_request = "a story about friendship and adventure"  # Safe fallback
            print(f"⚠️ {forbidden_msg}\nGenerating a safe alternative story instead.")
        else:
            safe_request = request

        # Get age-specific guidelines
        age_guidelines = AGE_GUIDELINES.get(age, AGE_GUIDELINES[7])  # Default to age 7 if not found
        
        # Format the prompt with safety guidelines
        prompt = GENERATION_PROMPT.format(
            request=safe_request,
            age=age,
            age_guidelines=age_guidelines,
            plan=plan,
            feedback="\n".join(feedback) if feedback else "No specific feedback to incorporate.",
            length=target_length,
            positive_themes=", ".join(POSITIVE_THEMES)
        )
        
        # Generate story with strong safety emphasis in system prompt
        response = call_llm(
            client=self.client,
            system_prompt_content="""You are an expert children's story writer specializing in safe, 
            age-appropriate content. You must NEVER include inappropriate topics like drugs, violence, 
            adult relationships, or scary content. Focus only on positive, wholesome themes suitable for children.""",
            user_prompt_content=prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
        # Verify the generated story is safe and age-appropriate
        has_forbidden, forbidden_msg = self._contains_forbidden_content(response)
        is_age_appropriate, age_msg = self._is_age_appropriate(response, age)
        
        if has_forbidden or not is_age_appropriate:
            # If the story is inappropriate, generate a safe replacement
            print(f"⚠️ Generated story contained inappropriate content or language.")
            print(f"Generating a safe replacement story...")
            
            # Generate a new story with stricter controls
            response = call_llm(
                client=self.client,
                system_prompt_content="""You are an expert children's story writer with a 
                strong focus on safety and age-appropriateness. Generate a simple, wholesome 
                story about friendship, kindness, or learning.""",
                user_prompt_content=f"Create a safe, age-appropriate story for a {age}-year-old about friendship and kindness.",
                max_tokens=1500,
                temperature=0.5  # Lower temperature for more predictable output
            )
        
        return response 