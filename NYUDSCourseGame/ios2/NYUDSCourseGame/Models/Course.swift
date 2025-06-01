import Foundation

enum CourseCategory: String, CaseIterable, Identifiable {
    case core = "Core"
    case aiResearch = "AI Research"
    case specialized = "Specialized"
    case industry = "Industry & Ethics"
    
    var id: String { self.rawValue }
}

enum CourseDifficulty: String, CaseIterable, Identifiable {
    case beginner = "Beginner"
    case intermediate = "Intermediate"
    case advanced = "Advanced"
    
    var id: String { self.rawValue }
}

struct Course: Identifiable, Codable {
    let id: String
    let code: String
    let title: String
    let description: String
    let category: CourseCategory
    let difficulty: CourseDifficulty
    let aiResearchRelevance: Int // 1-5 scale
    let prerequisites: [String]
    var isCompleted: Bool
    var progress: Double // 0-1
    var flashcards: [Flashcard]
    
    init(id: String = UUID().uuidString,
         code: String,
         title: String,
         description: String,
         category: CourseCategory,
         difficulty: CourseDifficulty,
         aiResearchRelevance: Int,
         prerequisites: [String] = [],
         isCompleted: Bool = false,
         progress: Double = 0,
         flashcards: [Flashcard] = []) {
        self.id = id
        self.code = code
        self.title = title
        self.description = description
        self.category = category
        self.difficulty = difficulty
        self.aiResearchRelevance = aiResearchRelevance
        self.prerequisites = prerequisites
        self.isCompleted = isCompleted
        self.progress = progress
        self.flashcards = flashcards
    }
} 