import Foundation
import Combine

enum DataServiceError: Error {
    case saveFailed
    case loadFailed
    case dataCorrupted
    
    var localizedDescription: String {
        switch self {
        case .saveFailed: return "Failed to save data"
        case .loadFailed: return "Failed to load data"
        case .dataCorrupted: return "Data is corrupted"
        }
    }
}

class DataService {
    private let userDefaults = UserDefaults.standard
    private let userKey = "userData"
    private let coursesKey = "coursesData"
    
    // MARK: - User Data
    
    func saveUser(_ user: User) -> AnyPublisher<Void, Error> {
        Future<Void, Error> { [weak self] promise in
            guard let self = self else {
                promise(.failure(DataServiceError.saveFailed))
                return
            }
            
            do {
                let encoder = JSONEncoder()
                let data = try encoder.encode(user)
                self.userDefaults.set(data, forKey: self.userKey)
                promise(.success(()))
            } catch {
                promise(.failure(DataServiceError.saveFailed))
            }
        }
        .eraseToAnyPublisher()
    }
    
    func loadUser() -> AnyPublisher<User, Error> {
        Future<User, Error> { [weak self] promise in
            guard let self = self else {
                promise(.failure(DataServiceError.loadFailed))
                return
            }
            
            guard let data = self.userDefaults.data(forKey: self.userKey) else {
                // Return default user if no data exists
                let defaultUser = User(name: "New Student")
                promise(.success(defaultUser))
                return
            }
            
            do {
                let decoder = JSONDecoder()
                let user = try decoder.decode(User.self, from: data)
                promise(.success(user))
            } catch {
                promise(.failure(DataServiceError.dataCorrupted))
            }
        }
        .eraseToAnyPublisher()
    }
    
    // MARK: - Courses Data
    
    func saveCourses(_ courses: [Course]) -> AnyPublisher<Void, Error> {
        Future<Void, Error> { [weak self] promise in
            guard let self = self else {
                promise(.failure(DataServiceError.saveFailed))
                return
            }
            
            do {
                let encoder = JSONEncoder()
                let data = try encoder.encode(courses)
                self.userDefaults.set(data, forKey: self.coursesKey)
                promise(.success(()))
            } catch {
                promise(.failure(DataServiceError.saveFailed))
            }
        }
        .eraseToAnyPublisher()
    }
    
    func loadCourses() -> AnyPublisher<[Course], Error> {
        Future<[Course], Error> { [weak self] promise in
            guard let self = self else {
                promise(.failure(DataServiceError.loadFailed))
                return
            }
            
            guard let data = self.userDefaults.data(forKey: self.coursesKey) else {
                // Return default courses if no data exists
                let defaultCourses = self.createDefaultCourses()
                promise(.success(defaultCourses))
                return
            }
            
            do {
                let decoder = JSONDecoder()
                let courses = try decoder.decode([Course].self, from: data)
                promise(.success(courses))
            } catch {
                promise(.failure(DataServiceError.dataCorrupted))
            }
        }
        .eraseToAnyPublisher()
    }
    
    // MARK: - Default Data
    
    private func createDefaultCourses() -> [Course] {
        return [
            // Core Courses
            Course(
                code: "DS-GA 1001",
                title: "Introduction to Data Science",
                description: "Fundamental concepts and tools for data science",
                category: .core,
                difficulty: .beginner,
                aiResearchRelevance: 0.3,
                flashcards: [
                    Flashcard(
                        question: "What is the difference between supervised and unsupervised learning?",
                        answer: "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.",
                        difficulty: .medium
                    ),
                    Flashcard(
                        question: "What is cross-validation?",
                        answer: "A technique to evaluate model performance by splitting data into training and validation sets multiple times.",
                        difficulty: .easy
                    )
                ]
            ),
            
            // AI Research Courses
            Course(
                code: "DS-GA 1003",
                title: "Machine Learning",
                description: "Advanced machine learning algorithms and applications",
                category: .aiResearch,
                difficulty: .intermediate,
                aiResearchRelevance: 0.9,
                flashcards: [
                    Flashcard(
                        question: "What is the difference between gradient descent and stochastic gradient descent?",
                        answer: "Gradient descent uses the entire dataset to compute the gradient, while SGD uses a single random sample.",
                        difficulty: .hard
                    ),
                    Flashcard(
                        question: "What is the bias-variance tradeoff?",
                        answer: "The tradeoff between a model's ability to fit the training data (bias) and its ability to generalize to new data (variance).",
                        difficulty: .medium
                    )
                ]
            ),
            
            // Specialized Courses
            Course(
                code: "DS-GA 1011",
                title: "Natural Language Processing",
                description: "Techniques for processing and understanding human language",
                category: .specialized,
                difficulty: .advanced,
                aiResearchRelevance: 0.8,
                flashcards: [
                    Flashcard(
                        question: "What is the transformer architecture?",
                        answer: "A neural network architecture that uses self-attention mechanisms to process sequential data.",
                        difficulty: .hard
                    ),
                    Flashcard(
                        question: "What is word embedding?",
                        answer: "A technique to represent words as vectors in a continuous space, capturing semantic relationships.",
                        difficulty: .medium
                    )
                ]
            ),
            
            // Industry & Ethics Courses
            Course(
                code: "DS-GA 1005",
                title: "Ethics and Privacy in Data Science",
                description: "Ethical considerations and privacy issues in data science",
                category: .industryAndEthics,
                difficulty: .intermediate,
                aiResearchRelevance: 0.4,
                flashcards: [
                    Flashcard(
                        question: "What is differential privacy?",
                        answer: "A system for publicly sharing information about a dataset while withholding information about individuals.",
                        difficulty: .medium
                    ),
                    Flashcard(
                        question: "What are the main ethical concerns in AI?",
                        answer: "Bias, transparency, accountability, privacy, and the impact on employment and society.",
                        difficulty: .easy
                    )
                ]
            )
        ]
    }
} 