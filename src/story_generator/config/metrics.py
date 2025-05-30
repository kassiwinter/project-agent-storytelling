"""Configuration for story evaluation metrics and specifications."""

from dataclasses import dataclass
from typing import Dict, List
from .genres import STORY_GENRES

@dataclass
class CreativityMetrics:
    originality: float  # How unique and fresh the story elements are
    imagination: float  # Level of imaginative elements and scenarios
    surprise_factor: float  # Unexpected but delightful story elements
    world_building: float  # Richness of the story's setting and atmosphere
    character_uniqueness: float  # How distinctive and memorable characters are

@dataclass
class StoryMetrics:
    # Core story components
    character_relatability: float
    plot_structure: float
    moral_lesson_clarity: float
    engagement_level: float
    language_development: float
    cognitive_elements: float
    age_appropriate_vocabulary: float
    attention_span_fit: float
    emotional_safety: float
    
    # Creativity components
    originality: float
    imagination: float
    surprise_factor: float
    world_building: float
    character_uniqueness: float

    @property
    def overall_score(self) -> float:
        """Calculate overall score using weights from config."""
        return sum(
            getattr(self, metric) * weight 
            for metric, weight in METRIC_WEIGHTS.items()
        )

    @property
    def creativity_score(self) -> float:
        """Calculate creativity-specific score."""
        creativity_metrics = {
            'originality': 0.25,
            'imagination': 0.25,
            'surprise_factor': 0.2,
            'world_building': 0.15,
            'character_uniqueness': 0.15
        }
        return sum(
            getattr(self, metric) * weight 
            for metric, weight in creativity_metrics.items()
        )

# Base weights for different components in overall score calculation
BASE_METRIC_WEIGHTS = {
    'character_relatability': 0.11,
    'plot_structure': 0.11,
    'moral_lesson_clarity': 0.11,
    'engagement_level': 0.11,
    'language_development': 0.07,
    'cognitive_elements': 0.07,
    'age_appropriate_vocabulary': 0.07,
    'attention_span_fit': 0.035,
    'emotional_safety': 0.035,
    # Creativity metrics (base weights)
    'originality': 0.07,
    'imagination': 0.07,
    'surprise_factor': 0.06,
    'world_building': 0.04,
    'character_uniqueness': 0.04
}

# Genre-specific metric adjustments
GENRE_METRIC_ADJUSTMENTS = {
    "FICTION": {
        "character_relatability": +0.1,
        "plot_structure": +0.05,
        "moral_lesson_clarity": +0.05,
        "world_building": -0.05
    },
    "FANTASY": {
        "imagination": +0.1,
        "world_building": +0.1,
        "originality": +0.05,
        "language_development": -0.05
    },
    "MYSTERY": {
        "cognitive_elements": +0.1,
        "engagement_level": +0.1,
        "surprise_factor": +0.05,
        "emotional_safety": -0.05
    },
    "HISTORICAL_FICTION": {
        "language_development": +0.1,
        "world_building": +0.1,
        "character_uniqueness": -0.05
    },
    "COMEDY_HUMOR": {
        "engagement_level": +0.15,
        "surprise_factor": +0.1,
        "moral_lesson_clarity": -0.05
    },
    "ADVENTURE": {
        "plot_structure": +0.05,
        "engagement_level": +0.05,
        "surprise_factor": +0.05,
        "moral_lesson_clarity": -0.05
    },
    "SCIENCE_FICTION": {
        "world_building": +0.1,
        "imagination": +0.1,
        "cognitive_elements": +0.05,
        "character_relatability": -0.05
    },
    "NONFICTION": {
        "language_development": +0.15,
        "cognitive_elements": +0.1,
        "world_building": -0.05
    },
    "ANIMAL_STORIES": {
        "character_uniqueness": +0.05,
        "emotional_safety": +0.05,
        "engagement_level": +0.05,
        "world_building": -0.05
    },
    "FAMILY_FRIENDSHIP": {
        "character_relatability": +0.1,
        "moral_lesson_clarity": +0.1,
        "emotional_safety": +0.05,
        "world_building": -0.05
    },
    "LEARNING_DISCOVERY": {
        "language_development": +0.1,
        "cognitive_elements": +0.1,
        "moral_lesson_clarity": +0.05,
        "imagination": -0.05
    },
    "CLASSIC_FAIRY_TALE": {
        "imagination": +0.1,
        "world_building": +0.05,
        "originality": -0.1  # Less emphasis on originality for classic tales
    }
}

# Base quality thresholds
BASE_QUALITY_THRESHOLDS = {
    'character_relatability': 0.7,
    'plot_structure': 0.7,
    'moral_lesson_clarity': 0.6,
    'engagement_level': 0.7,
    'language_development': 0.6,
    'cognitive_elements': 0.6,
    'age_appropriate_vocabulary': 0.8,
    'attention_span_fit': 0.7,
    'emotional_safety': 0.9,
    # Creativity thresholds
    'originality': 0.6,
    'imagination': 0.6,
    'surprise_factor': 0.5,
    'world_building': 0.6,
    'character_uniqueness': 0.6
}

def get_adjusted_metrics(genre: str = None) -> Dict:
    """Get metric weights adjusted for specific genre."""
    weights = BASE_METRIC_WEIGHTS.copy()
    if genre and genre.upper() in GENRE_METRIC_ADJUSTMENTS:
        adjustments = GENRE_METRIC_ADJUSTMENTS[genre.upper()]
        # Apply adjustments
        for metric, adjustment in adjustments.items():
            weights[metric] = max(0.0, min(1.0, weights[metric] + adjustment))
        
        # Normalize weights to ensure they sum to 1.0
        total_weight = sum(weights.values())
        if total_weight != 0:
            weights = {k: v/total_weight for k, v in weights.items()}
    
    return weights

# Current active weights (will be updated based on genre)
METRIC_WEIGHTS = BASE_METRIC_WEIGHTS.copy()

# Storage configuration
DEFAULT_METRICS_STORAGE = "story_metrics.json"

# Maximum number of revision cycles
MAX_REVISION_CYCLES = 3

# Minimum improvement threshold (to continue revisions)
MIN_IMPROVEMENT_THRESHOLD = 0.05

# Number of top stories to return in analysis
TOP_STORIES_COUNT = 5 