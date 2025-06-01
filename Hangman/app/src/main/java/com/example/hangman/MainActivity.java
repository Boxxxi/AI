package com.example.hangman;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

/**
 * Main activity for the Hangman game.
 */
public class MainActivity extends AppCompatActivity {
    private HangmanGame game;
    private TextView wordTextView;
    private TextView guessedLettersTextView;
    private ImageView hangmanImageView;
    private GridLayout lettersGridLayout;
    
    // Array of hangman state drawable resources
    private final int[] hangmanStates = {
            R.drawable.hangman_0,
            R.drawable.hangman_1,
            R.drawable.hangman_2,
            R.drawable.hangman_3,
            R.drawable.hangman_4,
            R.drawable.hangman_5,
            R.drawable.hangman_6
    };
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Get references to views
        wordTextView = findViewById(R.id.wordTextView);
        guessedLettersTextView = findViewById(R.id.guessedLettersTextView);
        hangmanImageView = findViewById(R.id.hangmanImageView);
        lettersGridLayout = findViewById(R.id.lettersGridLayout);
        
        // Set up New Game button
        Button newGameButton = findViewById(R.id.newGameButton);
        newGameButton.setOnClickListener(v -> startNewGame());
        
        // Start a new game
        startNewGame();
    }
    
    /**
     * Starts a new game.
     */
    private void startNewGame() {
        // Create a new game
        game = new HangmanGame();
        
        // Update the UI
        updateWordDisplay();
        updateGuessedLettersDisplay();
        updateHangmanImage();
        
        // Create letter buttons
        createLetterButtons();
    }
    
    /**
     * Creates buttons for all letters A-Z.
     */
    private void createLetterButtons() {
        // Clear existing buttons
        lettersGridLayout.removeAllViews();
        
        // Create a button for each letter A-Z
        for (char c = 'A'; c <= 'Z'; c++) {
            final char letter = c;
            
            // Inflate button from layout
            Button button = (Button) LayoutInflater.from(this)
                    .inflate(R.layout.letter_button, lettersGridLayout, false);
            
            // Set the letter
            button.setText(String.valueOf(letter));
            
            // Ensure button has correct style for current theme
            if (isDarkTheme()) {
                button.setTextColor(getResources().getColor(R.color.light_text, getTheme()));
            }
            
            // Set click listener
            button.setOnClickListener(v -> onLetterButtonClicked(letter, button));
            
            // Add to grid
            lettersGridLayout.addView(button);
        }
    }
    
    /**
     * Handles a letter button click.
     * @param letter The letter that was clicked
     * @param button The button that was clicked
     */
    private void onLetterButtonClicked(char letter, Button button) {
        // Make a guess with this letter
        boolean correct = game.guess(letter);
        
        // Disable the button
        button.setEnabled(false);
        
        // Change button color based on correctness and theme
        if (correct) {
            button.setBackgroundColor(getResources().getColor(isDarkTheme() ? R.color.dark_green : R.color.green, getTheme()));
        } else {
            button.setBackgroundColor(getResources().getColor(isDarkTheme() ? R.color.dark_red : R.color.red, getTheme()));
        }
        
        // Update the UI
        updateWordDisplay();
        updateGuessedLettersDisplay();
        updateHangmanImage();
        
        // Check if the game is over
        if (game.isGameOver()) {
            showGameOverDialog();
        }
    }
    
    /**
     * Updates the word display with the current state.
     */
    private void updateWordDisplay() {
        wordTextView.setText(game.getWordState());
    }
    
    /**
     * Updates the display of guessed letters.
     */
    private void updateGuessedLettersDisplay() {
        StringBuilder sb = new StringBuilder();
        
        for (Character c : game.getGuessedLettersList()) {
            sb.append(c).append(" ");
        }
        
        guessedLettersTextView.setText(sb.toString().trim());
    }
    
    /**
     * Updates the hangman image based on the number of wrong guesses.
     */
    private void updateHangmanImage() {
        hangmanImageView.setImageResource(hangmanStates[game.getWrongGuesses()]);
    }
    
    /**
     * Shows a dialog when the game is over.
     */
    private void showGameOverDialog() {
        // Inflate the dialog layout
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_game_over, null);
        
        // Get references to dialog views
        TextView titleTextView = dialogView.findViewById(R.id.titleTextView);
        TextView messageTextView = dialogView.findViewById(R.id.messageTextView);
        Button playAgainButton = dialogView.findViewById(R.id.playAgainButton);
        
        // Set dialog content based on game outcome
        if (game.hasPlayerWon()) {
            titleTextView.setText(R.string.congratulations);
            titleTextView.setTextColor(getResources().getColor(isDarkTheme() ? R.color.dark_green : R.color.green, getTheme()));
            messageTextView.setText(getString(R.string.you_won, game.getWord()));
        } else {
            titleTextView.setText(R.string.game_over);
            titleTextView.setTextColor(getResources().getColor(isDarkTheme() ? R.color.dark_red : R.color.red, getTheme()));
            messageTextView.setText(getString(R.string.you_lost, game.getWord()));
        }
        
        // Create and show the dialog
        AlertDialog.Builder builder = new AlertDialog.Builder(this, R.style.GameOverDialogStyle);
        builder.setView(dialogView);
        AlertDialog dialog = builder.create();
        
        // Set click listener for Play Again button
        playAgainButton.setOnClickListener(v -> {
            dialog.dismiss();
            startNewGame();
        });
        
        dialog.show();
    }
    
    /**
     * Checks if the app is currently using a dark theme.
     * @return true if using dark theme, false otherwise
     */
    private boolean isDarkTheme() {
        return (getResources().getConfiguration().uiMode & 
                android.content.res.Configuration.UI_MODE_NIGHT_MASK) == 
                android.content.res.Configuration.UI_MODE_NIGHT_YES;
    }
} 