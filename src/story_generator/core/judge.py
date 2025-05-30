"""Story judging and evaluation agent."""

from typing import Dict, List, Tuple
from openai import OpenAI
from ..utils.llm_utils import call_llm
from ..config.metrics import (
    METRIC_WEIGHTS, BASE_QUALITY_THRESHOLDS, 
    StoryMetrics,
    get_adjusted_metrics,
    MAX_REVISION_CYCLES,
    MIN_IMPROVEMENT_THRESHOLD
)
from ..config.genres import STORY_GENRES

JUDGE_PROMPT = """You are an expert children's story judge. Analyze this story and provide:
1. Numerical scores (0.0-1.0) for each component
2. Specific feedback for improvement that can be used to regenerate a better version
3. Final judgment on story acceptability

STORY:
{story}

TARGET AGE: {age}
GENRE: {genre_info}

Score each component from 0.0 (poor) to 1.0 (excellent):

CORE METRICS:
1. Character Relatability (Weight: {weights[character_relatability]}):
- Are characters age-appropriate and relatable?
- Do they face realistic challenges?
- Can children identify with their emotions?

2. Plot Structure (Weight: {weights[plot_structure]}):
- Clear beginning, middle, and end?
- Appropriate pacing for age?
- Engaging but not overstimulating?

3. Moral Lesson Clarity (Weight: {weights[moral_lesson_clarity]}):
- Clear but not preachy message?
- Age-appropriate complexity?
- Positive values reinforcement?

4. Engagement Level (Weight: {weights[engagement_level]}):
- Maintains interest throughout?
- Interactive elements?
- Memorable moments?

5. Language Development (Weight: {weights[language_development]}):
- Age-appropriate vocabulary?
- New word introduction?
- Clear sentence structures?

6. Cognitive Elements (Weight: {weights[cognitive_elements]}):
- Problem-solving opportunities?
- Critical thinking moments?
- Memory and prediction elements?

7. Age-Appropriate Vocabulary (Weight: {weights[age_appropriate_vocabulary]}):
- Word complexity matches age?
- New words properly contextualized?
- Consistent language level?

8. Attention Span Fit (Weight: {weights[attention_span_fit]}):
- Length appropriate for age?
- Pacing matches attention capacity?
- Engaging elements well-distributed?

9. Emotional Safety (Weight: {weights[emotional_safety]}):
- Appropriate emotional intensity?
- Safe conflict resolution?
- Comforting overall tone?

CREATIVITY METRICS:
10. Originality (Weight: {weights[originality]}):
- Fresh and unique story elements?
- Avoids common tropes?
- Creative problem-solving?

11. Imagination (Weight: {weights[imagination]}):
- Rich imaginative elements?
- Creative scenarios?
- Inspiring wonder?

12. Surprise Factor (Weight: {weights[surprise_factor]}):
- Unexpected twists?
- Delightful surprises?
- Novel story elements?

13. World Building (Weight: {weights[world_building]}):
- Rich setting details?
- Immersive atmosphere?
- Consistent story world?

14. Character Uniqueness (Weight: {weights[character_uniqueness]}):
- Distinctive personality traits?
- Memorable characteristics?
- Unique character voice?

Note: Each component must meet these minimum scores:
{thresholds}

FORMAT YOUR RESPONSE AS JSON:
{{
    "scores": {{
        "character_relatability": 0.0-1.0,
        "plot_structure": 0.0-1.0,
        "moral_lesson_clarity": 0.0-1.0,
        "engagement_level": 0.0-1.0,
        "language_development": 0.0-1.0,
        "cognitive_elements": 0.0-1.0,
        "age_appropriate_vocabulary": 0.0-1.0,
        "attention_span_fit": 0.0-1.0,
        "emotional_safety": 0.0-1.0,
        "originality": 0.0-1.0,
        "imagination": 0.0-1.0,
        "surprise_factor": 0.0-1.0,
        "world_building": 0.0-1.0,
        "character_uniqueness": 0.0-1.0
    }},
    "feedback": [
        "Specific improvement suggestions that can be used to regenerate the story"
    ],
    "judgment": "APPROVED" or "NEEDS_REVISION"
}}"""

class StoryJudge:
    def __init__(self, client: OpenAI):
        self.client = client
        self.revision_history = []

    def evaluate_story(
        self, 
        story: str, 
        age: int, 
        genre: str = None,
        revision_count: int = 0
    ) -> Tuple[StoryMetrics, List[str], str]:
        """Evaluate a story and provide metrics, feedback, and judgment."""
        # Get genre info
        genre_key = genre.upper() if genre else None
        genre_info = STORY_GENRES.get(genre_key, {"name": "Not specified", "description": "General story"})
        
        # Adjust weights based on genre
        weights = get_adjusted_metrics(genre_key)
        
        prompt = JUDGE_PROMPT.format(
            story=story,
            age=age,
            genre_info=f"{genre_info['name']}: {genre_info['description']}",
            weights=weights,
            thresholds=BASE_QUALITY_THRESHOLDS
        )
        
        # Get evaluation from GPT
        response = call_llm(
            client=self.client,
            system_prompt_content="You are an expert children's story judge. Respond only with the requested JSON format.",
            user_prompt_content=prompt,
            max_tokens=1000,
            temperature=0.3
        )
        
        try:
            # Parse the response
            result = eval(response)
            
            # Create metrics object
            metrics = StoryMetrics(**result['scores'])
            
            # Store metrics for improvement tracking
            self.revision_history.append(metrics)
            
            # Determine if we should continue revising
            if revision_count >= MAX_REVISION_CYCLES:
                return metrics, result['feedback'], "APPROVED"
                
            if self.needs_revision(metrics) and self.has_improvement_potential(metrics):
                return metrics, result['feedback'], "NEEDS_REVISION"
                
            return metrics, result['feedback'], "APPROVED"
            
        except Exception as e:
            raise ValueError(f"Failed to parse judge response: {e}")
    
    def needs_revision(self, metrics: StoryMetrics) -> bool:
        """Check if any metrics fall below quality thresholds."""
        for metric, threshold in BASE_QUALITY_THRESHOLDS.items():
            if getattr(metrics, metric) < threshold:
                return True
        return False
    
    def has_improvement_potential(self, metrics: StoryMetrics) -> bool:
        """Check if there's potential for meaningful improvement."""
        if len(self.revision_history) < 2:
            return True
            
        previous_metrics = self.revision_history[-2]
        current_metrics = self.revision_history[-1]
        
        # Calculate improvement in both overall and creativity scores
        overall_improvement = current_metrics.overall_score - previous_metrics.overall_score
        creativity_improvement = current_metrics.creativity_score - previous_metrics.creativity_score
        
        return (overall_improvement > MIN_IMPROVEMENT_THRESHOLD or 
                creativity_improvement > MIN_IMPROVEMENT_THRESHOLD)
    
    def get_genre_suggestions(self, story_idea: str) -> List[Dict]:
        """Suggest appropriate genres based on the story idea."""
        suggestions = []
        for genre_key, genre_info in STORY_GENRES.items():
            # Check if any keywords from the genre match the story idea
            if any(keyword.lower() in story_idea.lower() 
                  for keyword in genre_info["keywords"]):
                suggestions.append({
                    "key": genre_key,
                    "name": genre_info["name"],
                    "description": genre_info["description"],
                    "keywords": genre_info["keywords"]
                })
        return suggestions if suggestions else [{"key": "FICTION", **STORY_GENRES["FICTION"]}]  # Default to fiction if no match 