import SwiftUI

struct StatsView: View {
    @ObservedObject var viewModel: GameViewModel
    
    var body: some View {
        ScrollView {
            VStack(spacing: Theme.spacing.large) {
                // Overall Progress
                overallProgressSection
                
                // Course Progress
                courseProgressSection
                
                // Flashcard Stats
                flashcardStatsSection
                
                // Study Habits
                studyHabitsSection
            }
            .padding()
        }
        .navigationTitle("Statistics")
    }
    
    private var overallProgressSection: some View {
        VStack(alignment: .leading, spacing: Theme.spacing.medium) {
            Text("Overall Progress")
                .font(Theme.fonts.title2)
            
            HStack {
                VStack(alignment: .leading) {
                    Text("Level \(viewModel.user.level)")
                        .font(Theme.fonts.title3)
                    
                    Text("\(viewModel.user.experience) / \(viewModel.user.experienceToNextLevel) XP")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                AnimatedProgressBar(
                    progress: viewModel.user.progressToNextLevel,
                    color: Theme.colors.primary
                )
                .frame(width: 100)
            }
            
            StreakCalendarView(
                streak: viewModel.user.dailyStreak,
                lastStudyDate: viewModel.user.lastStudyDate
            )
        }
        .cardStyle()
    }
    
    private var courseProgressSection: some View {
        VStack(alignment: .leading, spacing: Theme.spacing.medium) {
            Text("Course Progress")
                .font(Theme.fonts.title2)
            
            ForEach(CourseCategory.allCases, id: \.self) { category in
                let categoryCourses = viewModel.courses.filter { $0.category == category }
                let completedCourses = categoryCourses.filter { viewModel.user.completedCourses.contains($0.id) }
                let progress = categoryCourses.isEmpty ? 0.0 : Double(completedCourses.count) / Double(categoryCourses.count)
                
                VStack(alignment: .leading) {
                    HStack {
                        Text(category.rawValue)
                            .font(Theme.fonts.headline)
                        
                        Spacer()
                        
                        Text("\(completedCourses.count)/\(categoryCourses.count)")
                            .font(Theme.fonts.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    AnimatedProgressBar(
                        progress: progress,
                        color: Theme.colors.forCategory(category)
                    )
                }
            }
        }
        .cardStyle()
    }
    
    private var flashcardStatsSection: some View {
        VStack(alignment: .leading, spacing: Theme.spacing.medium) {
            Text("Flashcard Stats")
                .font(Theme.fonts.title2)
            
            let totalFlashcards = viewModel.courses.reduce(0) { $0 + $1.flashcards.count }
            let masteredFlashcards = viewModel.user.masteredFlashcards.count
            
            HStack {
                VStack(alignment: .leading) {
                    Text("Mastered")
                        .font(Theme.fonts.headline)
                    
                    Text("\(masteredFlashcards) of \(totalFlashcards) flashcards")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                AnimatedProgressBar(
                    progress: totalFlashcards == 0 ? 0.0 : Double(masteredFlashcards) / Double(totalFlashcards),
                    color: Theme.colors.accent
                )
                .frame(width: 100)
            }
            
            // Difficulty Distribution
            VStack(alignment: .leading) {
                Text("By Difficulty")
                    .font(Theme.fonts.headline)
                
                ForEach(FlashcardDifficulty.allCases, id: \.self) { difficulty in
                    let difficultyCount = viewModel.courses.reduce(0) { $0 + $1.flashcards.filter { $0.difficulty == difficulty }.count }
                    let masteredCount = viewModel.courses.reduce(0) { $0 + $1.flashcards.filter { $0.difficulty == difficulty && viewModel.user.masteredFlashcards.contains($0.id) }.count }
                    
                    HStack {
                        Text(difficulty.rawValue)
                            .font(Theme.fonts.caption)
                        
                        Spacer()
                        
                        Text("\(masteredCount)/\(difficultyCount)")
                            .font(Theme.fonts.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
        }
        .cardStyle()
    }
    
    private var studyHabitsSection: some View {
        VStack(alignment: .leading, spacing: Theme.spacing.medium) {
            Text("Study Habits")
                .font(Theme.fonts.title2)
            
            // Daily Streak
            HStack {
                Image(systemName: "flame.fill")
                    .foregroundColor(.orange)
                
                Text("Current Streak: \(viewModel.user.dailyStreak) days")
                    .font(Theme.fonts.headline)
            }
            
            // Average Study Time
            HStack {
                Image(systemName: "clock.fill")
                    .foregroundColor(.blue)
                
                Text("Average Study Time: 30 min/day")
                    .font(Theme.fonts.headline)
            }
            
            // Most Active Time
            HStack {
                Image(systemName: "chart.bar.fill")
                    .foregroundColor(.green)
                
                Text("Most Active: Evening (6-9 PM)")
                    .font(Theme.fonts.headline)
            }
        }
        .cardStyle()
    }
}

// MARK: - Preview
struct StatsView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            StatsView(viewModel: GameViewModel())
        }
    }
} 