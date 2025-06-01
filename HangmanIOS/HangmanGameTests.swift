import XCTest

class HangmanGameTests: XCTestCase {
    
    func testGameInitialization() {
        let game = HangmanGame(word: "TEST")
        XCTAssertEqual(game.getWord(), "TEST")
        XCTAssertEqual(game.getWordState(), "_ _ _ _")
        XCTAssertEqual(game.getWrongGuesses(), 0)
        XCTAssertFalse(game.isGameOver())
        XCTAssertFalse(game.hasPlayerWon())
    }
    
    func testCorrectGuess() {
        let game = HangmanGame(word: "TEST")
        XCTAssertTrue(game.guess(letter: "T"))
        XCTAssertEqual(game.getWordState(), "T _ _ T")
        XCTAssertEqual(game.getWrongGuesses(), 0)
    }
    
    func testWrongGuess() {
        let game = HangmanGame(word: "TEST")
        XCTAssertFalse(game.guess(letter: "X"))
        XCTAssertEqual(game.getWordState(), "_ _ _ _")
        XCTAssertEqual(game.getWrongGuesses(), 1)
    }
    
    func testRepeatedGuess() {
        let game = HangmanGame(word: "TEST")
        XCTAssertTrue(game.guess(letter: "T"))
        XCTAssertFalse(game.guess(letter: "T")) // Should return false for repeated guess
        XCTAssertEqual(game.getWrongGuesses(), 0)
    }
    
    func testGameWin() {
        let game = HangmanGame(word: "TEST")
        XCTAssertTrue(game.guess(letter: "T"))
        XCTAssertTrue(game.guess(letter: "E"))
        XCTAssertTrue(game.guess(letter: "S"))
        XCTAssertTrue(game.isGameOver())
        XCTAssertTrue(game.hasPlayerWon())
    }
    
    func testGameLose() {
        let game = HangmanGame(word: "TEST")
        for letter in ["X", "Y", "Z", "W", "U", "V"] {
            XCTAssertFalse(game.guess(letter: Character(letter)))
        }
        XCTAssertTrue(game.isGameOver())
        XCTAssertFalse(game.hasPlayerWon())
    }
    
    func testGuessedLettersList() {
        let game = HangmanGame(word: "TEST")
        game.guess(letter: "T")
        game.guess(letter: "E")
        game.guess(letter: "X")
        let guessedLetters = game.getGuessedLettersList()
        XCTAssertEqual(guessedLetters, ["E", "T", "X"])
    }
} 