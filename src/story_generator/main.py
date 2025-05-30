"""

Future enhancements could focus on expanding the story delivery options to create a more
interactive and accessible experience.

Adding support for multiple output formats such as:
    1. audio narration (using text-to-speech models)
    2. illustrated versions (using DALL-E or similar image generation models) 
    3. interactive picture books

This would make the stories more engaging for different learning styles and preferences.
The system could be enhanced to ask users upfront about their preferred story format and
automatically generate the appropriate media, potentially including background music for
audio versions or animated elements for digital picture books.

Additional improvements could include voice customization for audio narration, style
selection for illustrations (e.g., watercolor, cartoon, realistic), and interactive elements
where children could make choices that influence the story's direction. 


"""

from .core.planner import StoryPlanner
from .core.generator import StoryGenerator
from .core.judge import StoryJudge
from .utils.llm_utils import initialize_openai_client

def main():
    """Main application logic."""
    # Give Introduction
    print("🌟 Welcome to the Magical Bedtime Story Generator! 🌟")
    print("By: Kassi Winter, creating perfect bedtime stories for ages 5-10!")
    print("-" * 60)

    # Initialize OpenAI client
    client = initialize_openai_client()

    # Initialize our agents
    planner = StoryPlanner(client)
    generator = StoryGenerator(client)
    judge = StoryJudge(client)

    # Get story request
    user_input = input("What kind of magical bedtime story would you like to hear tonight? 🌙\n> ")
    if not user_input.strip():
        print("Oops! You didn't specify a story. Please try again.")
        return

    # Get age for customization
    while True:
        try:
            age = int(input("What age is this story for? (5-10): "))
            if 5 <= age <= 10:
                break
            print("Please enter an age between 5 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    print("\n1. 📝 Planning your story...")
    story_plan = planner.create_outline(user_input, age)
    
    print("\n2. ✨ Creating your story...")
    story = generator.generate_story(user_input, age, story_plan)
    
    print("\n3. 🎯 Evaluating the story...")
    metrics, feedback, judgment = judge.evaluate_story(story, age)
    
    print("\n--- Your Personalized Bedtime Story ---")
    print(story)
    print("--- End of Story ---")
    
    print(f"\n📊 Story Evaluation Scores:")
    for metric, value in vars(metrics).items():
        if not metric.startswith('_'):  # Skip internal attributes
            print(f"- {metric.replace('_', ' ').title()}: {value:.2f}")
    print(f"Overall Score: {metrics.overall_score:.2f}")

    # Check both the LLM judgment and metric thresholds
    needs_revision = judgment == "NEEDS_REVISION" or judge.needs_revision(metrics)

    if needs_revision:
        print("\n✍️ Making some improvements based on feedback...")
        print("Feedback received:")
        for item in feedback:
            print(f"- {item}")
            
        print("\n4. 🌟 Generating improved version...")
        improved_story = generator.generate_story(
            user_input, 
            age, 
            story_plan,
            feedback=feedback
        )
        
        print("\n--- Your Improved Bedtime Story ---")
        print(improved_story)
        print("--- End of Story ---")
        
        # Re-evaluate the improved story
        improved_metrics, improved_feedback, improved_judgment = judge.evaluate_story(improved_story, age)
        print(f"\n📊 Improved Story Evaluation Scores:")
        for metric, value in vars(improved_metrics).items():
            if not metric.startswith('_'):
                print(f"- {metric.replace('_', ' ').title()}: {value:.2f}")
        print(f"Overall Score: {improved_metrics.overall_score:.2f}")
    else:
        print("\n✨ Perfect! The story meets all quality criteria!")

    print("\n🌙 Sweet dreams! Your perfect bedtime story is ready! 💫")

if __name__ == "__main__":
    main() 