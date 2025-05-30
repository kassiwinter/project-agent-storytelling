"""Utilities for age-related functionality."""

def get_age_from_user() -> int:
    """
    Get age for better story customization.
    
    Returns:
        int: The age of the listener (between 5-10)
    """
    while True:
        age_input = input("\nHow old is the listener? (5-10, or press Enter for 7): ").strip()
        
        if not age_input:  # Default
            return 7
        
        try:
            age = int(age_input)
            if 5 <= age <= 10:
                return age
            else:
                print("Please enter an age between 5 and 10.")
        except ValueError:
            print("Please enter a valid number.")

def get_age_appropriate_settings(age: int) -> dict:
    """
    Get age-appropriate story settings.
    
    Args:
        age: The age of the listener
        
    Returns:
        dict: Dictionary containing age-appropriate settings
    """
    if age <= 6:
        return {
            "length_guide": "250-350 words",
            "language_guide": "simple words and short sentences",
            "complexity": "very simple language and short sentences"
        }
    elif age <= 8:
        return {
            "length_guide": "350-450 words",
            "language_guide": "clear language with some descriptive details",
            "complexity": "age-appropriate vocabulary with descriptive details"
        }
    else:
        return {
            "length_guide": "450-600 words",
            "language_guide": "richer vocabulary and detailed descriptions",
            "complexity": "expanded vocabulary and more detailed descriptions"
        } 