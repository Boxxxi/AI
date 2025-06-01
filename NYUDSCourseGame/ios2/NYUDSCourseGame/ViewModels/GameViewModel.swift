import Foundation
import SwiftUI
import Combine

class GameViewModel: ObservableObject {
    @Published var user: User
    @Published var courses: [Course]
    @Published var currentCourse: Course?
    @Published var currentFlashcard: Flashcard?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    
    private let dataService: DataService
    private var cancellables = Set<AnyCancellable>()
    
    init(dataService: DataService = DataService()) {
        self.dataService = dataService
        self.user = User(name: "New Student")
        self.courses = []
        
        // Load initial data
        loadInitialData()
    }
    
    // MARK: - Data Loading
    
    private func loadInitialData() {
        isLoading = true
        
        // Load user data
        dataService.loadUser()
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                if case .failure(let error) = completion {
                    self?.errorMessage = "Failed to load user data: \(error.localizedDescription)"
                }
                self?.isLoading = false
            }, receiveValue: { [weak self] loadedUser in
                self?.user = loadedUser
            })
            .store(in: &cancellables)
        
        // Load courses
        dataService.loadCourses()
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                if case .failure(let error) = completion {
                    self?.errorMessage = "Failed to load courses: \(error.localizedDescription)"
                }
            }, receiveValue: { [weak self] loadedCourses in
                self?.courses = loadedCourses
            })
            .store(in: &cancellables)
    }
    
    // MARK: - Course Management
    
    func selectCourse(_ course: Course) {
        currentCourse = course
    }
    
    func startCourseStudy(_ course: Course) {
        selectCourse(course)
        // Load first flashcard
        if let firstFlashcard = course.flashcards.first {
            currentFlashcard = firstFlashcard
        }
    }
    
    func completeCourse(_ course: Course) {
        guard let index = courses.firstIndex(where: { $0.id == course.id }) else { return }
        
        var updatedCourse = course
        updatedCourse.isCompleted = true
        updatedCourse.progress = 1.0
        courses[index] = updatedCourse
        
        user.completeCourse(course.id)
        saveData()
    }
    
    // MARK: - Flashcard Management
    
    func answerFlashcard(correct: Bool) {
        guard let course = currentCourse,
              let flashcard = currentFlashcard,
              let courseIndex = courses.firstIndex(where: { $0.id == course.id }),
              let flashcardIndex = course.flashcards.firstIndex(where: { $0.id == flashcard.id }) else { return }
        
        // Update flashcard mastery
        var updatedFlashcard = flashcard
        updatedFlashcard.updateMastery(correct: correct)
        
        // Update course progress
        var updatedCourse = course
        updatedCourse.flashcards[flashcardIndex] = updatedFlashcard
        
        // Calculate new course progress
        let masteredCount = updatedCourse.flashcards.filter { $0.masteryLevel == .mastered }.count
        updatedCourse.progress = Double(masteredCount) / Double(updatedCourse.flashcards.count)
        
        // Update course completion status
        if updatedCourse.progress >= 1.0 {
            updatedCourse.isCompleted = true
            user.completeCourse(course.id)
        }
        
        courses[courseIndex] = updatedCourse
        
        // Move to next flashcard or complete course
        if let nextIndex = updatedCourse.flashcards.firstIndex(where: { $0.masteryLevel != .mastered }) {
            currentFlashcard = updatedCourse.flashcards[nextIndex]
        } else {
            currentFlashcard = nil
            completeCourse(updatedCourse)
        }
        
        // Update user's daily streak
        user.updateDailyStreak()
        
        // Save changes
        saveData()
    }
    
    // MARK: - User Management
    
    func updateUserName(_ newName: String) {
        user.name = newName
        saveData()
    }
    
    func resetProgress() {
        user = User(name: user.name)
        courses = courses.map { course in
            var updatedCourse = course
            updatedCourse.isCompleted = false
            updatedCourse.progress = 0.0
            updatedCourse.flashcards = updatedCourse.flashcards.map { flashcard in
                var updatedFlashcard = flashcard
                updatedFlashcard.masteryLevel = .notStarted
                updatedFlashcard.lastReviewed = nil
                updatedFlashcard.nextReviewDate = nil
                return updatedFlashcard
            }
            return updatedCourse
        }
        saveData()
    }
    
    // MARK: - Data Persistence
    
    private func saveData() {
        dataService.saveUser(user)
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                if case .failure(let error) = completion {
                    self?.errorMessage = "Failed to save user data: \(error.localizedDescription)"
                }
            }, receiveValue: { _ in })
            .store(in: &cancellables)
        
        dataService.saveCourses(courses)
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                if case .failure(let error) = completion {
                    self?.errorMessage = "Failed to save courses: \(error.localizedDescription)"
                }
            }, receiveValue: { _ in })
            .store(in: &cancellables)
    }
    
    // MARK: - Helper Methods
    
    func filteredCourses(category: CourseCategory? = nil, searchText: String = "") -> [Course] {
        courses.filter { course in
            let matchesCategory = category == nil || course.category == category
            let matchesSearch = searchText.isEmpty || 
                course.title.localizedCaseInsensitiveContains(searchText) ||
                course.code.localizedCaseInsensitiveContains(searchText)
            return matchesCategory && matchesSearch
        }
    }
    
    func coursesForAIResearchPath() -> [Course] {
        courses.filter { course in
            course.category == .aiResearch || course.category == .core
        }
    }
} 