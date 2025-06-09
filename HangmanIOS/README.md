# Hangman Game iOS

This is an iOS version of the classic Hangman word-guessing game, ported from a Java Android implementation.

## Features

- Clean, modern UI for iOS devices
- Same word list and game logic as the Android version
- Simple touch interface with onscreen keyboard
- Visual hangman display that updates as you play
- Game over alerts that tell you the word if you lose
- Support for both light and dark mode
- Responsive layout for all iOS devices

## Requirements

- iOS 15.0+
- Xcode 14.0+
- Swift 5.0+
- CocoaPods (for dependency management)

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/HangmanIOS.git
cd HangmanIOS
```

2. Open `HangmanIOS.xcodeproj` in Xcode
3. Build and run the project on your iOS device or simulator

## Development Setup

### Prerequisites

1. Install Xcode from the Mac App Store
2. Install CocoaPods if not already installed:
```bash
sudo gem install cocoapods
```

### Building the Project

1. Open the project in Xcode:
```bash
open HangmanIOS.xcodeproj
```

2. Select your target device (simulator or physical device)
3. Press ⌘B to build the project
4. Press ⌘R to run the project

### Running Tests

1. Open the project in Xcode
2. Press ⌘U to run all tests
3. View test results in the Test Navigator (⌘6)

## Project Structure

```
HangmanIOS/
├── Model/                    # Game logic and data
│   ├── HangmanGame.swift    # Core game mechanics
│   └── WordList.swift       # Word list management
├── View/                    # UI components
│   └── Main.storyboard      # Main UI layout
├── Controller/              # View controllers
│   └── ViewController.swift # Main game controller
├── Resources/              # Assets and resources
│   ├── Assets.xcassets     # Image assets
│   └── Info.plist         # App configuration
└── HangmanIOSTests/        # Test suite
    └── HangmanGameTests.swift
```

### Key Components

#### Model Layer
- `HangmanGame.swift`: Manages game state, word selection, and game logic
- `WordList.swift`: Handles word list management and random word selection

#### View Layer
- `Main.storyboard`: Contains the UI layout with:
  - Hangman figure display
  - Word display
  - On-screen keyboard
  - Game status indicators

#### Controller Layer
- `ViewController.swift`: Coordinates between model and view:
  - Handles user input
  - Updates UI
  - Manages game state
  - Shows alerts and messages

## Game Play

1. The app selects a random word from a list of over 200 words
2. Guess letters by tapping the on-screen keyboard
3. Correct guesses reveal the corresponding letters in the word
4. Incorrect guesses add a part to the hangman figure
5. You win if you guess the entire word before the hangman is complete
6. You lose if the hangman figure is completed before you guess the word

## Development Guidelines

### Code Style
- Follow Swift style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Testing
- Write unit tests for game logic
- Test UI components
- Verify game state transitions
- Test edge cases

### Performance
- Optimize image assets
- Minimize memory usage
- Ensure smooth animations
- Handle device rotation properly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is open source and available under the MIT License. 