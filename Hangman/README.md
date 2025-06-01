# Hangman Game for Android

A classic Hangman word guessing game implemented for Android devices featuring:
- A corpus of 200+ English words greater than 6 letters
- Smooth vector graphics animation of the hangman progression
- Interactive letter selection with visual feedback
- Win/loss state tracking with game statistics
- Clean, intuitive user interface

<img src="screenshots/game_screenshot.png" alt="Game Screenshot" width="300"/>

## Features

- **Random Word Selection**: Words are randomly selected from a curated list of English words
- **Visual Feedback**: Letter buttons change color based on correct/incorrect guesses
- **Progressive Difficulty**: With longer words and limited guesses
- **Hangman Visualization**: Vector-based hangman graphics that progressively appear with incorrect guesses
- **Game Completion Dialog**: Shows game outcome and reveals the word

## Project Structure

### Source Code
- `app/src/main/java/com/example/hangman/`
  - `MainActivity.java` - UI controller that handles user interaction
  - `HangmanGame.java` - Core game logic and state management
  - `WordList.java` - Word corpus and random selection

### Resources
- `app/src/main/res/`
  - `layout/` - UI layouts (activity_main.xml, letter_button.xml, dialog_game_over.xml)
  - `drawable/` - Vector graphics for hangman states (hangman_0.xml through hangman_6.xml)
  - `values/` - String resources, colors, and theme definitions

## Installation

### Prerequisites
- Android Studio
- Android SDK with minimum API level 26 (Android 8.0 Oreo)
- Gradle 8.10 or higher
- Java 17

### Steps to Build and Run
1. Clone this repository:
   ```
   git clone https://github.com/Boxxxi/Hangman_android.git
   ```

2. Open the project in Android Studio

3. Sync the project with Gradle files:
   - Click on "File" > "Sync Project with Gradle Files"

4. Build the project:
   - Click on "Build" > "Make Project"

5. Run on an emulator or physical device:
   - Click on "Run" > "Run 'app'"
   - Select a device or create a new virtual device

### Direct APK Installation
1. Download the latest release APK from the [Releases](https://github.com/Boxxxi/Hangman_android/releases) section
2. Enable installation from unknown sources in your device settings
3. Open the APK file on your device to install

## How to Play

1. Start a new game by launching the app or tapping "New Game"
2. A random word will be selected and displayed as underscores
3. Tap on letter buttons to guess letters in the word
4. If the letter is in the word:
   - It will be revealed in its correct position(s)
   - The letter button will turn green
5. If the letter is not in the word:
   - Part of the hangman will be drawn
   - The letter button will turn red
6. Continue guessing until you either:
   - Successfully guess the entire word (you win!)
   - Make 6 incorrect guesses and complete the hangman (you lose)
7. After the game ends, a dialog will show your result and the correct word
8. Tap "Play Again" to start a new game with a different word

## Technical Implementation

- Built with Java for Android
- Uses modern Android development practices including:
  - Constraint layouts for responsive design
  - Vector drawables for smooth scaling on all devices
  - Clean separation of game logic and UI
  - Efficient word state representation
  - Optimized resource usage

## Troubleshooting

- **App crashes on startup**: Ensure your device runs Android 8.0 or newer
- **Letter buttons don't respond**: Check if you've already guessed that letter
- **Word display appears incorrect**: Report as an issue with the specific word
- **Performance issues**: Close other applications running in the background

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

### Development Guidelines
- Follow existing code style and patterns
- Add comments for complex logic
- Update README if adding major features
- Add appropriate tests for new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Word list compiled from multiple English language sources
- Inspired by the classic Hangman paper and pencil game
- Thanks to all contributors and testers
