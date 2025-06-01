package com.example.hangman;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * This class contains the main game logic for the Hangman game.
 */
public class HangmanGame {
    // Maximum number of wrong guesses allowed
    private static final int MAX_WRONG_GUESSES = 6;
    
    // The word to guess
    private final String word;
    
    // Set of letters that have been guessed
    private final Set<Character> guessedLetters;
    
    // Number of wrong guesses so far
    private int wrongGuesses;
    
    // Game state
    private boolean gameOver;
    private boolean playerWon;
    
    /**
     * Creates a new Hangman game with a random word.
     */
    public HangmanGame() {
        this(WordList.getRandomWord());
    }
    
    /**
     * Creates a new Hangman game with the specified word.
     * @param word The word to guess (will be converted to uppercase)
     */
    public HangmanGame(String word) {
        this.word = word.toUpperCase();
        this.guessedLetters = new HashSet<>();
        this.wrongGuesses = 0;
        this.gameOver = false;
        this.playerWon = false;
    }
    
    /**
     * Makes a guess of the specified letter.
     * @param letter The letter to guess (case insensitive)
     * @return true if the letter is in the word, false otherwise
     */
    public boolean guess(char letter) {
        if (gameOver) {
            return false;
        }
        
        // Convert to uppercase
        letter = Character.toUpperCase(letter);
        
        // Check if the letter has already been guessed
        if (guessedLetters.contains(letter)) {
            return false;
        }
        
        // Add the letter to the set of guessed letters
        guessedLetters.add(letter);
        
        // Check if the letter is in the word
        boolean correctGuess = word.indexOf(letter) >= 0;
        
        // If the guess is wrong, increment the wrong guess counter
        if (!correctGuess) {
            wrongGuesses++;
            
            // Check if the player has reached the maximum number of wrong guesses
            if (wrongGuesses >= MAX_WRONG_GUESSES) {
                gameOver = true;
                playerWon = false;
            }
        } else {
            // Check if the player has won
            if (isWordGuessed()) {
                gameOver = true;
                playerWon = true;
            }
        }
        
        return correctGuess;
    }
    
    /**
     * Returns the current state of the word, with unguessed letters replaced by underscores.
     * @return The current state of the word
     */
    public String getWordState() {
        StringBuilder result = new StringBuilder();
        
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            
            if (guessedLetters.contains(c)) {
                result.append(c);
            } else {
                result.append('_');
            }
            
            result.append(' ');
        }
        
        return result.toString().trim();
    }
    
    /**
     * Returns the set of letters that have been guessed.
     * @return The set of guessed letters
     */
    public Set<Character> getGuessedLetters() {
        return new HashSet<>(guessedLetters);
    }
    
    /**
     * Returns a list of all letters that have been used, in alphabetical order.
     * @return A list of guessed letters
     */
    public List<Character> getGuessedLettersList() {
        List<Character> result = new ArrayList<>(guessedLetters);
        java.util.Collections.sort(result);
        return result;
    }
    
    /**
     * Returns the number of wrong guesses so far.
     * @return The number of wrong guesses
     */
    public int getWrongGuesses() {
        return wrongGuesses;
    }
    
    /**
     * Returns whether the game is over.
     * @return true if the game is over, false otherwise
     */
    public boolean isGameOver() {
        return gameOver;
    }
    
    /**
     * Returns whether the player has won.
     * @return true if the player has won, false otherwise
     */
    public boolean hasPlayerWon() {
        return playerWon;
    }
    
    /**
     * Returns the word to guess.
     * @return The word to guess
     */
    public String getWord() {
        return word;
    }
    
    /**
     * Checks if the word has been fully guessed.
     * @return true if the word has been guessed, false otherwise
     */
    private boolean isWordGuessed() {
        for (int i = 0; i < word.length(); i++) {
            if (!guessedLetters.contains(word.charAt(i))) {
                return false;
            }
        }
        return true;
    }
} 