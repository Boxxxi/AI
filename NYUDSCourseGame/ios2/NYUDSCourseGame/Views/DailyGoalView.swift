import SwiftUI

struct DailyGoalView: View {
    @ObservedObject var viewModel: GameViewModel
    @State private var showingGoalSettings = false
    @State private var selectedGoal: Int = 10
    
    private let goalOptions = [5, 10, 15, 20, 25, 30]
    
    var body: some View {
        VStack(spacing: Theme.spacing.large) {
            // Progress Circle
            ZStack {
                Circle()
                    .stroke(Theme.colors.secondaryBackground, lineWidth: 20)
                    .frame(width: 200, height: 200)
                
                Circle()
                    .trim(from: 0, to: CGFloat(min(viewModel.user.dailyProgress, 1.0)))
                    .stroke(Theme.colors.primary, style: StrokeStyle(lineWidth: 20, lineCap: .round))
                    .frame(width: 200, height: 200)
                    .rotationEffect(.degrees(-90))
                    .animation(.easeInOut, value: viewModel.user.dailyProgress)
                
                VStack {
                    Text("\(Int(viewModel.user.dailyProgress * 100))%")
                        .font(.system(size: 40, weight: .bold, design: .rounded))
                    
                    Text("Daily Goal")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            // Stats
            HStack(spacing: Theme.spacing.extraLarge) {
                VStack {
                    Text("\(viewModel.user.todayCompleted)")
                        .font(Theme.fonts.title2)
                        .foregroundColor(Theme.colors.primary)
                    
                    Text("Completed")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
                
                VStack {
                    Text("\(selectedGoal)")
                        .font(Theme.fonts.title2)
                        .foregroundColor(Theme.colors.primary)
                    
                    Text("Goal")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
                
                VStack {
                    Text("\(viewModel.user.dailyStreak)")
                        .font(Theme.fonts.title2)
                        .foregroundColor(.orange)
                    
                    Text("Streak")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            // Progress Bar
            VStack(alignment: .leading, spacing: Theme.spacing.small) {
                HStack {
                    Text("Today's Progress")
                        .font(Theme.fonts.headline)
                    
                    Spacer()
                    
                    Text("\(viewModel.user.todayCompleted)/\(selectedGoal)")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
                
                AnimatedProgressBar(
                    progress: Double(viewModel.user.todayCompleted) / Double(selectedGoal),
                    color: Theme.colors.primary
                )
            }
            .padding()
            .background(Theme.colors.secondaryBackground)
            .cornerRadius(Theme.cornerRadius)
            
            // Settings Button
            Button(action: {
                showingGoalSettings = true
            }) {
                HStack {
                    Image(systemName: "gear")
                    Text("Change Daily Goal")
                }
                .font(Theme.fonts.headline)
                .foregroundColor(.white)
                .padding()
                .background(Theme.colors.primary)
                .cornerRadius(Theme.cornerRadius)
            }
        }
        .padding()
        .sheet(isPresented: $showingGoalSettings) {
            GoalSettingsView(selectedGoal: $selectedGoal, goalOptions: goalOptions)
        }
    }
}

struct GoalSettingsView: View {
    @Binding var selectedGoal: Int
    let goalOptions: [Int]
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Daily Flashcard Goal")) {
                    Picker("Number of Flashcards", selection: $selectedGoal) {
                        ForEach(goalOptions, id: \.self) { number in
                            Text("\(number) flashcards")
                        }
                    }
                }
                
                Section(header: Text("About Daily Goals")) {
                    Text("Setting a daily goal helps you maintain consistency in your learning. Try to complete your goal every day to build your streak!")
                        .font(Theme.fonts.caption)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("Daily Goal")
            .navigationBarItems(trailing: Button("Done") {
                presentationMode.wrappedValue.dismiss()
            })
        }
    }
}

// MARK: - Preview
struct DailyGoalView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            DailyGoalView(viewModel: GameViewModel())
        }
    }
} 