"""Utilities for genre detection and management."""

from ..config.genres import STORY_GENRES

def detect_story_genre(user_request: str) -> str:
    """
    Detect the best literary genre for the request using keyword matching.
    
    Args:
        user_request: The user's story request
        
    Returns:
        str: The detected genre key from STORY_GENRES
    """
    request_lower = user_request.lower()
    
    # Check for genre keywords
    for genre_key, genre_info in STORY_GENRES.items():
        if any(keyword in request_lower for keyword in genre_info["keywords"]):
            return genre_key
    
    # Smart fallbacks based on common storytelling patterns
    if any(word in request_lower for word in ["magic", "wizard", "dragon", "fairy", "spell", "enchanted"]):
        return "FANTASY"
    elif any(word in request_lower for word in ["funny", "silly", "laugh", "joke", "humor", "giggle"]):
        return "COMEDY_HUMOR"
    elif any(word in request_lower for word in ["mystery", "solve", "clue", "detective", "puzzle", "secret"]):
        return "MYSTERY"
    elif any(word in request_lower for word in ["adventure", "journey", "quest", "explore", "brave", "hero"]):
        return "ADVENTURE"
    elif any(word in request_lower for word in ["animal", "dog", "cat", "rabbit", "bear", "forest", "pet"]):
        return "ANIMAL_STORIES"
    elif any(word in request_lower for word in ["family", "friend", "mom", "dad", "sister", "brother"]):
        return "FAMILY_FRIENDSHIP"
    elif any(word in request_lower for word in ["space", "robot", "future", "alien", "technology"]):
        return "SCIENCE_FICTION"
    elif any(word in request_lower for word in ["long ago", "past", "history", "ancient", "old times"]):
        return "HISTORICAL_FICTION"
    elif any(word in request_lower for word in ["true", "real", "fact", "learn", "teach"]):
        return "NONFICTION"
    elif any(word in request_lower for word in ["princess", "prince", "castle", "once upon a time"]):
        return "CLASSIC_FAIRY_TALE"
    else:
        return "FICTION"  # Safe, versatile default 