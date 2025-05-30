"""

Modular Design: Code is split into logical modules for better maintainability
Clear Separation of Concerns: Each component has a specific responsibility
Configuration Management: Settings and constants are centralized
Utility Functions: Common functionality is extracted into utility modules
Documentation: Added README.md with clear instructions
Dependencies: Created requirements.txt for easy installation


"""

from .utils.llm_utils import initialize_openai_client
from .utils.age_utils import get_age_from_user
from .core.generator import generate_story
from .core.judge import judge_story
from .core.reviser import revise_story

def main():
    """Main application logic."""
    # Give Introduction
    print("🌟 Welcome to the Enhanced Bedtime Story Generator! 🌟")
    print("Kassi and Barnaby create perfect bedtime stories for ages 5-10!")
    print("-" * 60)

    # Initialize OpenAI client
    client = initialize_openai_client()

    # Get story request
    user_input = input("What kind of magical bedtime story would you like to hear tonight? 🌙\n> ")

    if not user_input.strip():
        print("Oops! You didn't specify a story. Please try again.")
        return

    # Get age for customization
    age = get_age_from_user()
    print(f"\n🎭 Creating a perfect bedtime story for a {age}-year-old...")

    # 1. Generate enhanced story
    story_v1 = generate_story(client, user_input, age)
    print(f"\n--- Your Personalized Bedtime Story ---")
    print(story_v1)
    print("--- End of Story ---")

    # 2. Judge with age-aware criteria  
    judgement = judge_story(client, story_v1, user_input, age)

    final_story = ""

    # 3. Handle revision if needed
    if judgement.startswith("STORY_APPROVED"):
        print(f"\n🎉 Barnaby says: This story is perfectly crafted for a {age}-year-old's bedtime!")
        final_story = story_v1
    elif judgement.startswith("STORY_NEEDS_REVISION"):
        print(f"\n📝 Barnaby has expert suggestions to perfect this bedtime story:")
        feedback_text = judgement.replace("STORY_NEEDS_REVISION\n", "", 1).strip()
        print(f"Expert feedback: {feedback_text}")
        
        # 4. Create enhanced revision
        story_v2 = revise_story(client, story_v1, user_input, feedback_text, age)
        print(f"\n--- Your Perfected Bedtime Story ---")
        print(story_v2)
        print("--- End of Perfected Story ---")
        print(f"\n✨ This polished version should be absolutely perfect for a {age}-year-old's bedtime!")
        final_story = story_v2
    else:
        print(f"\n🤔 The review was unclear, but here's your personalized story:")
        final_story = story_v1

    print(f"\n🌙 Sweet dreams! Your perfect bedtime story is ready! 💫")
    print("May it carry you off to the most wonderful dreams! 🌟")

if __name__ == "__main__":
    main() 