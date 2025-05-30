"""Content filtering configuration for story generation."""

# Topics that are strictly forbidden in children's stories
FORBIDDEN_TOPICS = {
    "SUBSTANCES": {
        "keywords": ["drugs", "alcohol", "smoking", "marijuana", "cigarettes", "weed", "tobacco"],
        "reason": "Substance use is not appropriate for children's stories"
    },
    "VIOLENCE": {
        "keywords": ["kill", "murder", "blood", "weapon", "gun", "knife", "death", "fighting"],
        "reason": "Violence can be traumatic for young readers"
    },
    "ADULT_CONTENT": {
        "keywords": ["sex", "romance", "dating", "kissing", "relationship", "love story"],
        "reason": "Adult relationships are not appropriate for children's stories"
    },
    "SCARY_CONTENT": {
        "keywords": ["horror", "ghost", "monster", "nightmare", "scary", "terror", "demon", "evil"],
        "reason": "Frightening content can cause anxiety in children"
    },
    "INAPPROPRIATE_BEHAVIOR": {
        "keywords": ["stealing", "lying", "cheating", "bullying", "mean", "cruel"],
        "reason": "Negative behaviors should not be glorified"
    }
}

# Age-appropriate theme guidelines
AGE_GUIDELINES = {
    5: {
        "language_level": "Simple words, short sentences, concrete concepts",
        "content_focus": "Family, friendship, simple daily activities",
        "emotional_depth": "Basic emotions, clear cause-and-effect",
        "conflict_level": "Very mild, easily resolved conflicts"
    },
    6: {
        "language_level": "Growing vocabulary, compound sentences",
        "content_focus": "School experiences, peer relationships",
        "emotional_depth": "Understanding others' feelings",
        "conflict_level": "Minor challenges with guidance"
    },
    7: {
        "language_level": "More complex sentences, new vocabulary in context",
        "content_focus": "Adventure, discovery, problem-solving",
        "emotional_depth": "Multiple perspectives, empathy",
        "conflict_level": "Problem-solving with support"
    },
    8: {
        "language_level": "Rich vocabulary, varied sentence structures",
        "content_focus": "Mystery, science, world exploration",
        "emotional_depth": "Complex emotions, moral reasoning",
        "conflict_level": "Independent problem-solving"
    },
    9: {
        "language_level": "Advanced vocabulary, complex ideas",
        "content_focus": "Personal growth, wider world understanding",
        "emotional_depth": "Nuanced emotions, ethical thinking",
        "conflict_level": "More complex challenges"
    },
    10: {
        "language_level": "Sophisticated language, abstract concepts",
        "content_focus": "Social issues, personal responsibility",
        "emotional_depth": "Deep emotional understanding",
        "conflict_level": "Real-world problems with guidance"
    }
}

# Positive themes to encourage
POSITIVE_THEMES = [
    "friendship",
    "kindness",
    "honesty",
    "courage",
    "perseverance",
    "respect",
    "responsibility",
    "creativity",
    "curiosity",
    "teamwork",
    "family bonds",
    "helping others",
    "learning",
    "nature appreciation",
    "problem-solving"
]

def is_age_appropriate(content: str, age: int) -> tuple[bool, str]:
    """Check if content is age-appropriate."""
    # Implementation will be in the StoryGenerator class
    pass

def contains_forbidden_content(content: str) -> tuple[bool, str]:
    """Check if content contains any forbidden topics."""
    # Implementation will be in the StoryGenerator class
    pass 