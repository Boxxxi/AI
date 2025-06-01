import Foundation

/**
 * This class contains the main game logic for the Hangman game.
 */
class HangmanGame {
    // Maximum number of wrong guesses allowed
    static let maxWrongGuesses = 6
    
    // The word to guess
    private let word: String
    
    // Set of letters that have been guessed
    private var guessedLetters = Set<Character>()
    
    // Number of wrong guesses so far
    private var wrongGuesses = 0
    
    // Game state
    private var gameOver = false
    private var playerWon = false
    
    /**
     * Creates a new Hangman game with a random word.
     */
    init() {
        self.word = WordList.getRandomWord()
    }
    
    /**
     * Creates a new Hangman game with the specified word.
     * @param word The word to guess (will be converted to uppercase)
     */
    init(word: String) {
        self.word = word.uppercased()
    }
    
    /**
     * Makes a guess of the specified letter.
     * @param letter The letter to guess (case insensitive)
     * @return true if the letter is in the word, false otherwise
     */
    func guess(letter: Character) -> Bool {
        if gameOver {
            return false
        }
        
        // Convert to uppercase
        let uppercaseLetter = Character(String(letter).uppercased())
        
        // Check if the letter has already been guessed
        if guessedLetters.contains(uppercaseLetter) {
            return false
        }
        
        // Add the letter to the set of guessed letters
        guessedLetters.insert(uppercaseLetter)
        
        // Check if the letter is in the word
        let correctGuess = word.contains(uppercaseLetter)
        
        // If the guess is wrong, increment the wrong guess counter
        if !correctGuess {
            wrongGuesses += 1
            
            // Check if the player has reached the maximum number of wrong guesses
            if wrongGuesses >= HangmanGame.maxWrongGuesses {
                gameOver = true
                playerWon = false
            }
        } else {
            // Check if the player has won
            if isWordGuessed() {
                gameOver = true
                playerWon = true
            }
        }
        
        return correctGuess
    }
    
    /**
     * Returns the current state of the word, with unguessed letters replaced by underscores.
     * @return The current state of the word
     */
    func getWordState() -> String {
        var result = ""
        
        for character in word {
            if guessedLetters.contains(character) {
                result.append(character)
            } else {
                result.append("_")
            }
            
            result.append(" ")
        }
        
        return result.trimmingCharacters(in: .whitespaces)
    }
    
    /**
     * Returns the set of letters that have been guessed.
     * @return The set of guessed letters
     */
    func getGuessedLetters() -> Set<Character> {
        return guessedLetters
    }
    
    /**
     * Returns an array of all letters that have been used, in alphabetical order.
     * @return An array of guessed letters
     */
    func getGuessedLettersList() -> [Character] {
        return guessedLetters.sorted()
    }
    
    /**
     * Returns the number of wrong guesses so far.
     * @return The number of wrong guesses
     */
    func getWrongGuesses() -> Int {
        return wrongGuesses
    }
    
    /**
     * Returns whether the game is over.
     * @return true if the game is over, false otherwise
     */
    func isGameOver() -> Bool {
        return gameOver
    }
    
    /**
     * Returns whether the player has won.
     * @return true if the player has won, false otherwise
     */
    func hasPlayerWon() -> Bool {
        return playerWon
    }
    
    /**
     * Returns the word to guess.
     * @return The word to guess
     */
    func getWord() -> String {
        return word
    }
    
    /**
     * Checks if the word has been fully guessed.
     * @return true if the word has been guessed, false otherwise
     */
    private func isWordGuessed() -> Bool {
        for character in word {
            if !guessedLetters.contains(character) {
                return false
            }
        }
        return true
    }
} 