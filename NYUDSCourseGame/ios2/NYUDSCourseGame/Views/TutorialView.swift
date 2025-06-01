import SwiftUI

struct TutorialView: View {
    @Binding var isPresented: Bool
    @State private var currentPage = 0
    
    private let pages = [
        TutorialPage(
            title: "Welcome to NYU DS Course Game!",
            description: "Learn and master your Data Science courses through interactive flashcards and gamification.",
            image: "graduationcap.fill"
        ),
        TutorialPage(
            title: "Courses",
            description: "Browse through all available courses, filter by category, and track your progress.",
            image: "book.fill"
        ),
        TutorialPage(
            title: "AI Research Path",
            description: "Follow a curated path of courses specifically designed for AI Research.",
            image: "brain.head.profile"
        ),
        TutorialPage(
            title: "Study Mode",
            description: "Practice with flashcards, track your mastery, and earn XP for your progress.",
            image: "rectangle.fill.on.rectangle.fill"
        ),
        TutorialPage(
            title: "Achievements",
            description: "Unlock achievements as you complete courses and master flashcards.",
            image: "star.fill"
        ),
        TutorialPage(
            title: "Daily Streak",
            description: "Maintain your learning streak by studying every day and earn bonus rewards.",
            image: "flame.fill"
        )
    ]
    
    var body: some View {
        VStack {
            TabView(selection: $currentPage) {
                ForEach(0..<pages.count, id: \.self) { index in
                    TutorialPageView(page: pages[index])
                        .tag(index)
                }
            }
            .tabViewStyle(PageTabViewStyle())
            .indexViewStyle(PageIndexViewStyle(backgroundDisplayMode: .always))
            
            HStack {
                if currentPage < pages.count - 1 {
                    Button(action: {
                        withAnimation {
                            currentPage += 1
                        }
                    }) {
                        Text("Next")
                            .font(Theme.fonts.headline)
                            .foregroundColor(.white)
                            .padding()
                            .background(Theme.colors.primary)
                            .cornerRadius(Theme.cornerRadius)
                    }
                } else {
                    Button(action: {
                        isPresented = false
                    }) {
                        Text("Get Started")
                            .font(Theme.fonts.headline)
                            .foregroundColor(.white)
                            .padding()
                            .background(Theme.colors.primary)
                            .cornerRadius(Theme.cornerRadius)
                    }
                }
            }
            .padding()
        }
        .background(Theme.colors.background)
    }
}

struct TutorialPage {
    let title: String
    let description: String
    let image: String
}

struct TutorialPageView: View {
    let page: TutorialPage
    
    var body: some View {
        VStack(spacing: Theme.spacing.large) {
            Image(systemName: page.image)
                .font(.system(size: 60))
                .foregroundColor(Theme.colors.primary)
                .padding()
            
            Text(page.title)
                .font(Theme.fonts.title)
                .multilineTextAlignment(.center)
            
            Text(page.description)
                .font(Theme.fonts.body)
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)
                .padding(.horizontal)
        }
        .padding()
    }
}

// MARK: - Preview
struct TutorialView_Previews: PreviewProvider {
    static var previews: some View {
        TutorialView(isPresented: .constant(true))
    }
} 