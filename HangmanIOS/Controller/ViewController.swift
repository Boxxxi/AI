import UIKit

class ViewController: UIViewController {
    
    // MARK: - Outlets
    @IBOutlet weak var hangmanImageView: UIImageView!
    @IBOutlet weak var wordLabel: UILabel!
    @IBOutlet weak var guessedLettersLabel: UILabel!
    @IBOutlet weak var keyboardContainerView: UIView!
    @IBOutlet weak var newGameButton: UIButton!
    
    // MARK: - Properties
    private var game: HangmanGame!
    private var letterButtons = [UIButton]()
    
    // Hangman state images
    private let hangmanImages = [
        UIImage(named: "hangman_0"),
        UIImage(named: "hangman_1"),
        UIImage(named: "hangman_2"),
        UIImage(named: "hangman_3"),
        UIImage(named: "hangman_4"),
        UIImage(named: "hangman_5"),
        UIImage(named: "hangman_6")
    ]
    
    // MARK: - Lifecycle Methods
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setupUI()
        setupKeyboard()
        newGameButton.addTarget(self, action: #selector(startNewGame), for: .touchUpInside)
        
        startNewGame()
    }
    
    // MARK: - Game Setup
    private func setupUI() {
        view.backgroundColor = .systemBackground
        
        // Configure word label
        wordLabel.font = UIFont.monospacedSystemFont(ofSize: 24, weight: .medium)
        wordLabel.textAlignment = .center
        
        // Configure guessed letters label
        guessedLettersLabel.font = UIFont.systemFont(ofSize: 16)
        guessedLettersLabel.textAlignment = .center
        
        // Configure new game button
        newGameButton.backgroundColor = .systemBlue
        newGameButton.layer.cornerRadius = 8
        newGameButton.setTitle("New Game", for: .normal)
        newGameButton.setTitleColor(.white, for: .normal)
    }
    
    private func setupKeyboard() {
        // Clear existing buttons
        letterButtons.forEach { $0.removeFromSuperview() }
        letterButtons.removeAll()
        
        // Create buttons for A-Z
        let buttonsPerRow = 7
        let buttonWidth = (keyboardContainerView.bounds.width - 10) / CGFloat(buttonsPerRow)
        let buttonHeight: CGFloat = 40
        
        let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        var row = 0
        var col = 0
        
        for letter in letters {
            let button = UIButton(type: .system)
            button.frame = CGRect(
                x: CGFloat(col) * buttonWidth,
                y: CGFloat(row) * (buttonHeight + 5),
                width: buttonWidth - 5,
                height: buttonHeight
            )
            
            button.setTitle(String(letter), for: .normal)
            button.titleLabel?.font = UIFont.systemFont(ofSize: 18, weight: .medium)
            button.layer.cornerRadius = 5
            button.backgroundColor = .systemGray5
            button.addTarget(self, action: #selector(letterButtonTapped(_:)), for: .touchUpInside)
            
            keyboardContainerView.addSubview(button)
            letterButtons.append(button)
            
            col += 1
            if col >= buttonsPerRow {
                col = 0
                row += 1
            }
        }
    }
    
    // MARK: - Game Actions
    @objc private func startNewGame() {
        game = HangmanGame()
        
        // Reset UI
        updateWordDisplay()
        updateGuessedLettersDisplay()
        updateHangmanImage()
        
        // Reset keyboard buttons
        letterButtons.forEach { button in
            button.isEnabled = true
            button.backgroundColor = .systemGray5
        }
    }
    
    @objc private func letterButtonTapped(_ sender: UIButton) {
        guard let letter = sender.title(for: .normal)?.first else { return }
        
        // Make a guess with this letter
        let correct = game.guess(letter: letter)
        
        // Disable the button and update its appearance
        sender.isEnabled = false
        sender.backgroundColor = correct ? .systemGreen : .systemRed
        
        // Update UI
        updateWordDisplay()
        updateGuessedLettersDisplay()
        updateHangmanImage()
        
        // Check if the game is over
        if game.isGameOver() {
            showGameOverAlert()
        }
    }
    
    // MARK: - UI Updates
    private func updateWordDisplay() {
        wordLabel.text = game.getWordState()
    }
    
    private func updateGuessedLettersDisplay() {
        let guessedLetters = game.getGuessedLettersList().map { String($0) }.joined(separator: " ")
        guessedLettersLabel.text = "Guessed: \(guessedLetters)"
    }
    
    private func updateHangmanImage() {
        let wrongGuesses = game.getWrongGuesses()
        if wrongGuesses >= 0 && wrongGuesses < hangmanImages.count {
            hangmanImageView.image = hangmanImages[wrongGuesses]
        }
    }
    
    private func showGameOverAlert() {
        let title = game.hasPlayerWon() ? "Congratulations!" : "Game Over"
        let message = game.hasPlayerWon() ? 
            "You correctly guessed the word!" : 
            "The word was: \(game.getWord())"
        
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: "Play Again", style: .default) { [weak self] _ in
            self?.startNewGame()
        })
        
        present(alert, animated: true)
    }
} 