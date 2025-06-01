import SwiftUI

struct HomeView: View {
    @ObservedObject var viewModel: GameViewModel
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // Courses Tab
            NavigationView {
                CoursesView(viewModel: viewModel)
            }
            .tabItem {
                Label("Courses", systemImage: "book.fill")
            }
            .tag(0)
            
            // AI Research Path Tab
            NavigationView {
                AIResearchPathView(viewModel: viewModel)
            }
            .tabItem {
                Label("AI Path", systemImage: "brain.head.profile")
            }
            .tag(1)
            
            // Study Tab
            NavigationView {
                if let course = viewModel.currentCourse {
                    FlashcardStudyView(viewModel: viewModel, course: course)
                } else {
                    Text("Select a course to start studying")
                        .font(.title2)
                        .foregroundColor(.secondary)
                }
            }
            .tabItem {
                Label("Study", systemImage: "graduationcap.fill")
            }
            .tag(2)
            
            // Profile Tab
            NavigationView {
                ProfileView(viewModel: viewModel)
            }
            .tabItem {
                Label("Profile", systemImage: "person.fill")
            }
            .tag(3)
        }
        .accentColor(.blue)
        .onAppear {
            // Set up the tab bar appearance
            let appearance = UITabBarAppearance()
            appearance.configureWithOpaqueBackground()
            UITabBar.appearance().standardAppearance = appearance
            UITabBar.appearance().scrollEdgeAppearance = appearance
        }
    }
}

// MARK: - Preview
struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView(viewModel: GameViewModel())
    }
} 