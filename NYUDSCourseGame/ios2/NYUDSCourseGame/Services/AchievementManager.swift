import Foundation
import Combine

class AchievementManager: ObservableObject {
    static let shared = AchievementManager()
    private let notificationManager = NotificationManager.shared
    
    private init() {}
    
    func checkAchievements(for user: User, courses: [Course]) {
        // Course Completion Achievements
        checkCourseCompletionAchievements(completedCourses: user.completedCourses.count)
        
        // Flashcard Mastery Achievements
        let masteredFlashcards = user.masteredFlashcards.count
        checkFlashcardMasteryAchievements(masteredCount: masteredFlashcards)
        
        // Streak Achievements
        checkStreakAchievements(streak: user.dailyStreak)
        
        // Level Achievements
        checkLevelAchievements(level: user.level)
        
        // Category Mastery Achievements
        checkCategoryMasteryAchievements(courses: courses, completedCourses: user.completedCourses)
    }
    
    private func checkCourseCompletionAchievements(completedCourses: Int) {
        let achievements = [
            (count: 1, title: "First Course", message: "Completed your first course"),
            (count: 5, title: "Course Explorer", message: "Completed 5 courses"),
            (count: 10, title: "Course Master", message: "Completed 10 courses")
        ]
        
        for achievement in achievements {
            if completedCourses >= achievement.count {
                unlockAchievement(
                    title: achievement.title,
                    message: achievement.message,
                    icon: "graduationcap.fill"
                )
            }
        }
    }
    
    private func checkFlashcardMasteryAchievements(masteredCount: Int) {
        let achievements = [
            (count: 10, title: "Flashcard Novice", message: "Mastered 10 flashcards"),
            (count: 50, title: "Flashcard Expert", message: "Mastered 50 flashcards"),
            (count: 100, title: "Flashcard Master", message: "Mastered 100 flashcards")
        ]
        
        for achievement in achievements {
            if masteredCount >= achievement.count {
                unlockAchievement(
                    title: achievement.title,
                    message: achievement.message,
                    icon: "rectangle.fill.on.rectangle.fill"
                )
            }
        }
    }
    
    private func checkStreakAchievements(streak: Int) {
        let achievements = [
            (days: 3, title: "Consistent Learner", message: "Maintained a 3-day streak"),
            (days: 7, title: "Dedicated Student", message: "Maintained a 7-day streak"),
            (days: 30, title: "Learning Champion", message: "Maintained a 30-day streak")
        ]
        
        for achievement in achievements {
            if streak >= achievement.days {
                unlockAchievement(
                    title: achievement.title,
                    message: achievement.message,
                    icon: "flame.fill"
                )
            }
        }
    }
    
    private func checkLevelAchievements(level: Int) {
        let achievements = [
            (level: 5, title: "Rising Star", message: "Reached level 5"),
            (level: 10, title: "Experienced Learner", message: "Reached level 10"),
            (level: 20, title: "Master Scholar", message: "Reached level 20")
        ]
        
        for achievement in achievements {
            if level >= achievement.level {
                unlockAchievement(
                    title: achievement.title,
                    message: achievement.message,
                    icon: "star.fill"
                )
            }
        }
    }
    
    private func checkCategoryMasteryAchievements(courses: [Course], completedCourses: [String]) {
        let categories = CourseCategory.allCases
        for category in categories {
            let categoryCourses = courses.filter { $0.category == category }
            let completedCategoryCourses = categoryCourses.filter { completedCourses.contains($0.id) }
            
            if completedCategoryCourses.count == categoryCourses.count {
                unlockAchievement(
                    title: "\(category.rawValue) Master",
                    message: "Completed all \(category.rawValue) courses",
                    icon: iconForCategory(category)
                )
            }
        }
    }
    
    private func iconForCategory(_ category: CourseCategory) -> String {
        switch category {
        case .core:
            return "book.fill"
        case .aiResearch:
            return "brain.head.profile"
        case .specialized:
            return "puzzlepiece.fill"
        case .industryAndEthics:
            return "hand.raised.fill"
        }
    }
    
    private func unlockAchievement(title: String, message: String, icon: String) {
        let notification = NotificationItem(
            title: "New Achievement: \(title)",
            message: message,
            type: .achievement,
            icon: icon
        )
        
        notificationManager.showNotification(notification)
    }
} 