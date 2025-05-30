# Magical Bedtime Story Generator 🌟

An AI-powered bedtime story generator that creates safe, engaging, and age-appropriate stories for children ages 5-10. Created by Kassi Winter.

## Features

- 📚 Age-appropriate story generation (ages 5-10)
- 🛡️ Multi-layered content safety filtering
- 📊 Comprehensive story evaluation system
- ✨ Automatic story improvement
- 🎯 Educational value scaling by age
- 🌈 Focus on positive themes and values

## Architecture

The system uses three specialized AI agents working together:
1. **Story Planner**: Creates detailed story outlines
2. **Story Generator**: Crafts engaging, safe stories
3. **Story Judge**: Evaluates and suggests improvements

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/project-agent-bedtime-storytelling.git
cd project-agent-bedtime-storytelling
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your configuration:
```bash
cp src/story_generator/config/settings.template.py src/story_generator/config/settings.py
```

5. Edit `src/story_generator/config/settings.py` and add your OpenAI API key.

## Usage

Run the story generator:
```bash
python -m src.story_generator.main
```

Follow the prompts to:
1. Enter your story request
2. Specify the target age (5-10)
3. Receive your personalized bedtime story!

## Safety Features

- Content filtering for age-appropriate material
- Forbidden topic detection
- Safe content generation
- Multiple safety verification layers
- Age-appropriate language checking

## Future Enhancements

- Audio narration support
- Illustrated versions using AI image generation
- Interactive picture books
- Voice customization
- Style selection for illustrations
- Interactive story choices

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
