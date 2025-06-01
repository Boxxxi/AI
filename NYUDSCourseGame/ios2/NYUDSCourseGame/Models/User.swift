import Foundation

struct Achievement: Identifiable, Codable {
    let id: String
    let title: String
    let description: String
    let iconName: String
    let xpReward: Int
    var isUnlocked: Bool
    var unlockedDate: Date?
    
    init(id: String = UUID().uuidString,
         title: String,
         description: String,
         iconName: String,
         xpReward: Int,
         isUnlocked: Bool = false,
         unlockedDate: Date? = nil) {
        self.id = id
        self.title = title
        self.description = description
        self.iconName = iconName
        self.xpReward = xpReward
        self.isUnlocked = isUnlocked
        self.unlockedDate = unlockedDate
    }
}

struct User: Identifiable, Codable {
    let id: String
    var name: String
    var level: Int
    var experience: Int
    var dailyStreak: Int
    var lastStudyDate: Date?
    var achievements: [Achievement]
    var completedCourses: [String] // Course IDs
    var masteredFlashcards: [String] // Flashcard IDs
    
    // Computed properties
    var experienceToNextLevel: Int {
        level * 1000 // Simple leveling system: 1000 XP per level
    }
    
    var progressToNextLevel: Double {
        Double(experience % experienceToNextLevel) / Double(experienceToNextLevel)
    }
    
    init(id: String = UUID().uuidString,
         name: String,
         level: Int = 1,
         experience: Int = 0,
         dailyStreak: Int = 0,
         lastStudyDate: Date? = nil,
         achievements: [Achievement] = [],
         completedCourses: [String] = [],
         masteredFlashcards: [String] = []) {
        self.id = id
        self.name = name
        self.level = level
        self.experience = experience
        self.dailyStreak = dailyStreak
        self.lastStudyDate = lastStudyDate
        self.achievements = achievements
        self.completedCourses = completedCourses
        self.masteredFlashcards = masteredFlashcards
    }
    
    mutating func addExperience(_ amount: Int) {
        experience += amount
        checkLevelUp()
    }
    
    mutating func checkLevelUp() {
        while experience >= experienceToNextLevel {
            level += 1
            experience -= experienceToNextLevel
        }
    }
    
    mutating func updateDailyStreak() {
        let calendar = Calendar.current
        let now = Date()
        
        if let lastDate = lastStudyDate {
            if calendar.isDateInToday(lastDate) {
                // Already studied today
                return
            } else if calendar.isDateInYesterday(lastDate) {
                // Studied yesterday, increment streak
                dailyStreak += 1
            } else {
                // Streak broken
                dailyStreak = 1
            }
        } else {
            // First study session
            dailyStreak = 1
        }
        
        lastStudyDate = now
    }
    
    mutating func completeCourse(_ courseId: String) {
        if !completedCourses.contains(courseId) {
            completedCourses.append(courseId)
            addExperience(500) // Base XP for completing a course
        }
    }
    
    mutating func masterFlashcard(_ flashcardId: String) {
        if !masteredFlashcards.contains(flashcardId) {
            masteredFlashcards.append(flashcardId)
            addExperience(10) // XP for mastering a flashcard
        }
    }
    
    mutating func unlockAchievement(_ achievementId: String) {
        if let index = achievements.firstIndex(where: { $0.id == achievementId }) {
            var achievement = achievements[index]
            if !achievement.isUnlocked {
                achievement.isUnlocked = true
                achievement.unlockedDate = Date()
                achievements[index] = achievement
                addExperience(achievement.xpReward)
            }
        }
    }
} 