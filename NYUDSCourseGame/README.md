# NYU DS Course Game

A gamified learning app designed to help NYU MS Data Science students prepare for their coursework while focusing on an AI Research career path. Available in both web and iOS versions.

## Overview

This application gamifies the learning process for NYU's Master of Science in Data Science program, with a special focus on courses that align with a career in AI Research. The app uses flashcards, achievements, progress tracking, and level-up mechanics to make learning more engaging and effective.

## Features

- **Career Path Focus**: Specialized learning track for AI Research career aspirations
- **Course Catalog**: All core and elective courses from NYU's MS DS program
- **Gamification Elements**:
  - Flashcard-based learning with mastery tracking
  - Experience points (XP) and level progression
  - Achievements for completing milestones
  - Daily challenges and streaks
- **Progress Tracking**: Visual progress for each course and your overall AI Research readiness
- **Course Categorization**: Courses organized by relevance to AI Research, difficulty, and category

## Project Structure

```
NYUDSCourseGame/
├── web/                    # Web implementation
│   ├── index.html         # Main web interface
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── assets/            # Images and other assets
└── ios2/                   # iOS implementation
    ├── NYUDSCourseGame/   # Main iOS app
    └── Testgame/          # Test suite
```

## NYU MS DS Courses for AI Research

This app includes real courses from NYU's MS in Data Science program, with special emphasis on those most relevant to AI Research:

### Core Foundations
- DS-GA 1001: Introduction to Data Science
- DS-GA 1002: Statistical and Mathematical Methods
- DS-GA 1003: Machine Learning
- DS-GA 1004: Big Data

### AI Research Track
- DS-GA 1008: Deep Learning 
- DS-GA 1011: Natural Language Processing with Representation Learning
- DS-GA 1005: Computer Vision
- DS-GA 3001: Reinforcement Learning
- DS-GA 3002: Advanced Topics in Deep Learning Research

### Mathematics for ML Research
- DS-GA 1013: Optimization Methods for Data Science
- DS-GA 1014: Computational Statistics

### Industry & Ethics
- DS-GA 1018: Natural Language Understanding and AI Ethics
- DS-GA 1019: Responsible Data Science

## Learning Path for AI Researchers

The app creates a guided learning path for aspiring AI researchers:

1. **Core Foundations**: Build your mathematical and statistical foundation
2. **Machine Learning Fundamentals**: Master the core ML concepts
3. **Deep Learning Specialization**: Advance to neural networks and deep learning
4. **Specialized AI Areas**: Focus on NLP, Computer Vision, or Reinforcement Learning
5. **Research Methods**: Learn how to conduct AI research and stay current

## Implementation Details

### Web Version
- Built with HTML5, CSS3, and JavaScript
- Responsive design for all devices
- Local storage for progress tracking
- No server-side dependencies

To run the web version:
1. Open `web/index.html` in a modern web browser
2. No additional setup required

### iOS Version
- Built with Swift and SwiftUI
- MVVM architecture
- Local data persistence with UserDefaults
- Native iOS features and animations

To run the iOS version:
1. Open `ios2/NYUDSCourseGame.xcodeproj` in Xcode
2. Build and run on iOS simulator or device

## How to Use

1. Browse courses by category or AI research relevance
2. Study flashcards for each course
3. Complete daily challenges to maintain your streak
4. Track your progress on the AI Research path
5. Earn achievements and level up as you master concepts

## Development

### Web Development
- Edit HTML/CSS/JS files in the `web` directory
- Test changes in a modern web browser
- No build process required

### iOS Development
- Use Xcode 14.0+ for development
- Follow Swift style guide
- Run tests using the Testgame target

## Future Enhancements

- Community features to connect with other NYU DS students
- Integration with research paper summaries
- More specialized career paths (ML Engineer, Data Engineer, etc.)
- Content updates with new courses as the program evolves
- Cross-platform synchronization
- Offline mode improvements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on both web and iOS platforms
5. Submit a pull request

## Acknowledgements

This app is designed specifically for NYU MS DS students with a focus on AI research career aspirations. Course information is based on the NYU Center for Data Science curriculum. 