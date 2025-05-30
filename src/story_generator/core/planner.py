"""Story planning agent that creates detailed outlines."""

from typing import Dict
from openai import OpenAI
from ..utils.llm_utils import call_llm

PLANNING_PROMPT = """You are an expert children's story planner. Create a detailed story outline incorporating these key elements:

USER REQUEST: {request}
TARGET AGE: {age}

Consider these critical components:

1. Characters:
- Design relatable, age-appropriate characters
- Give them clear emotional journeys
- Create opportunities for identification and empathy

2. Plot Structure:
- Beginning: Set up characters and setting (calm, engaging)
- Middle: Introduce gentle conflict/challenge
- End: Resolve conflict with positive message
- Ensure bedtime-appropriate pacing

3. Theme & Moral:
- Core message/lesson appropriate for age {age}
- Subtle teaching moments
- Positive values reinforcement

4. Engagement Elements:
- Sensory details for imagination
- Interactive moments
- Memory/prediction opportunities
- Age-appropriate humor

5. Language Development:
- Core vocabulary appropriate for age {age}
- 2-3 new vocabulary words to learn
- Clear, age-appropriate sentence structures

6. Cognitive Elements:
- Simple problem-solving opportunities
- Pattern recognition
- Cause-and-effect relationships
- Memory engagement

FORMAT YOUR RESPONSE AS:
{{
    "title": "Story Title",
    "characters": {{
        "main": {{
            "name": "Name",
            "description": "Brief description",
            "emotional_journey": "Character's emotional arc"
        }},
        "supporting": [
            {{
                "name": "Name",
                "role": "Role in story"
            }}
        ]
    }},
    "plot_outline": {{
        "setup": "Opening scene and situation",
        "challenge": "Main gentle conflict",
        "resolution": "How conflict is resolved",
        "ending": "Calming conclusion"
    }},
    "theme": {{
        "main_message": "Core lesson",
        "teaching_moments": [
            "Specific moments for learning"
        ]
    }},
    "engagement_elements": [
        "List of specific engaging moments"
    ],
    "vocabulary": {{
        "new_words": [
            {{
                "word": "new word",
                "context": "How it's introduced"
            }}
        ]
    }},
    "cognitive_elements": [
        "Specific learning opportunities"
    ]
}}"""

class StoryPlanner:
    def __init__(self, client: OpenAI):
        self.client = client
    
    def create_outline(self, request: str, age: int) -> Dict:
        """Create a detailed story outline."""
        prompt = PLANNING_PROMPT.format(
            request=request,
            age=age
        )
        
        # Get plan from GPT
        response = call_llm(
            client=self.client,
            system_prompt_content="You are an expert children's story planner. Respond only with the requested JSON format.",
            user_prompt_content=prompt,
            max_tokens=1000,
            temperature=0.7  # Allow some creativity
        )
        
        try:
            # Parse the response as JSON
            plan = eval(response)  # Safe since we control the input format
            return plan
        except Exception as e:
            raise ValueError(f"Failed to parse planning response: {e}")
            
    def validate_plan(self, plan: Dict, age: int) -> bool:
        """Validate that the plan meets our requirements."""
        checks = [
            len(plan['plot_outline']['setup']) > 0,
            len(plan['characters']['main']['description']) > 0,
            len(plan['theme']['teaching_moments']) > 0,
            len(plan['engagement_elements']) > 0,
            len(plan['vocabulary']['new_words']) <= 3,  # Max 3 new words
            all(len(word['context']) > 0 for word in plan['vocabulary']['new_words']),
            len(plan['cognitive_elements']) > 0
        ]
        
        return all(checks) 