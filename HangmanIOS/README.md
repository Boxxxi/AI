# Hangman Game iOS

This is an iOS version of the classic Hangman word-guessing game, ported from a Java Android implementation.

## Features

- Clean, modern UI for iOS devices
- Same word list and game logic as the Android version
- Simple touch interface with onscreen keyboard
- Visual hangman display that updates as you play
- Game over alerts that tell you the word if you lose

## Requirements

- iOS 15.0+
- Xcode 14.0+
- Swift 5.0+

## Installation

1. Clone this repository
2. Open `HangmanIOS.xcodeproj` in Xcode
3. Build and run the project on your iOS device or simulator

## Git Setup

The repository includes a comprehensive `.gitignore` file specifically configured for iOS/Swift development. This ensures that only necessary source files are tracked and build artifacts, user-specific settings, and other temporary files are excluded.

To initialize the repository:

```bash
# Navigate to the project directory
cd HangmanIOS

# Initialize git repository (if not already done)
git init

# Add all files respecting the gitignore
git add .

# Make initial commit
git commit -m "Initial commit of Hangman iOS app"

# Add remote repository (replace with your repository URL)
git remote add origin git@github.com:Boxxxi/Hangman_ios.git

# Push to remote repository
git push -u origin main
```

## Game Play

1. The app selects a random word from a list of over 200 words
2. Guess letters by tapping the on-screen keyboard
3. Correct guesses reveal the corresponding letters in the word
4. Incorrect guesses add a part to the hangman figure
5. You win if you guess the entire word before the hangman is complete
6. You lose if the hangman figure is completed before you guess the word

## Project Structure

- **Model**: Contains the game logic classes
  - `HangmanGame.swift`: Core game mechanics
  - `WordList.swift`: List of words and random word selection
- **View**: Contains UI elements
  - `Main.storyboard`: Main UI layout
- **Controller**: Contains view controllers
  - `ViewController.swift`: Main game controller
- **Resources**: Contains image assets and other resources

## Credits

This iOS implementation is based on the Java Android version of the Hangman game.

## License

This project is open source and available under the MIT License. 