import Foundation
import AVFoundation
import UIKit

class SoundManager {
    static let shared = SoundManager()
    private var audioPlayer: AVAudioPlayer?
    private let hapticGenerator = UINotificationFeedbackGenerator()
    private let impactGenerator = UIImpactFeedbackGenerator(style: .medium)
    
    private init() {
        setupAudioSession()
    }
    
    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.ambient, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Failed to set up audio session: \(error)")
        }
    }
    
    // MARK: - Sound Effects
    
    func playCorrectAnswer() {
        playSound(named: "correct")
        impactGenerator.impactOccurred()
    }
    
    func playWrongAnswer() {
        playSound(named: "wrong")
        impactGenerator.impactOccurred()
    }
    
    func playAchievementUnlocked() {
        playSound(named: "achievement")
        hapticGenerator.notificationOccurred(.success)
    }
    
    func playLevelUp() {
        playSound(named: "levelup")
        hapticGenerator.notificationOccurred(.success)
    }
    
    func playCourseCompleted() {
        playSound(named: "complete")
        hapticGenerator.notificationOccurred(.success)
    }
    
    private func playSound(named: String) {
        guard let url = Bundle.main.url(forResource: named, withExtension: "mp3") else {
            print("Sound file not found: \(named)")
            return
        }
        
        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.play()
        } catch {
            print("Failed to play sound: \(error)")
        }
    }
    
    // MARK: - Haptic Feedback
    
    func prepareHaptics() {
        hapticGenerator.prepare()
        impactGenerator.prepare()
    }
    
    func playHapticSuccess() {
        hapticGenerator.notificationOccurred(.success)
    }
    
    func playHapticWarning() {
        hapticGenerator.notificationOccurred(.warning)
    }
    
    func playHapticError() {
        hapticGenerator.notificationOccurred(.error)
    }
    
    func playImpactFeedback() {
        impactGenerator.impactOccurred()
    }
} 