import Foundation

enum FlashcardDifficulty: String, CaseIterable, Identifiable {
    case easy = "Easy"
    case medium = "Medium"
    case hard = "Hard"
    
    var id: String { self.rawValue }
}

enum MasteryLevel: Int, CaseIterable, Identifiable {
    case notStarted = 0
    case learning = 1
    case reviewing = 2
    case mastered = 3
    
    var id: Int { self.rawValue }
    
    var description: String {
        switch self {
        case .notStarted: return "Not Started"
        case .learning: return "Learning"
        case .reviewing: return "Reviewing"
        case .mastered: return "Mastered"
        }
    }
}

struct Flashcard: Identifiable, Codable {
    let id: String
    let question: String
    let answer: String
    let difficulty: FlashcardDifficulty
    var masteryLevel: MasteryLevel
    var lastReviewed: Date?
    var nextReviewDate: Date?
    
    init(id: String = UUID().uuidString,
         question: String,
         answer: String,
         difficulty: FlashcardDifficulty,
         masteryLevel: MasteryLevel = .notStarted,
         lastReviewed: Date? = nil,
         nextReviewDate: Date? = nil) {
        self.id = id
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.masteryLevel = masteryLevel
        self.lastReviewed = lastReviewed
        self.nextReviewDate = nextReviewDate
    }
    
    mutating func updateMastery(correct: Bool) {
        switch masteryLevel {
        case .notStarted:
            masteryLevel = .learning
        case .learning:
            masteryLevel = correct ? .reviewing : .learning
        case .reviewing:
            masteryLevel = correct ? .mastered : .learning
        case .mastered:
            if !correct {
                masteryLevel = .reviewing
            }
        }
        
        lastReviewed = Date()
        updateNextReviewDate()
    }
    
    private mutating func updateNextReviewDate() {
        let calendar = Calendar.current
        let now = Date()
        
        switch masteryLevel {
        case .notStarted:
            nextReviewDate = now
        case .learning:
            nextReviewDate = calendar.date(byAdding: .hour, value: 1, to: now)
        case .reviewing:
            nextReviewDate = calendar.date(byAdding: .day, value: 1, to: now)
        case .mastered:
            nextReviewDate = calendar.date(byAdding: .weekOfYear, value: 1, to: now)
        }
    }
} 