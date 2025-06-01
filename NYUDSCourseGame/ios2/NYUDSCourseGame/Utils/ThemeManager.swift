import SwiftUI

struct Theme {
    static let colors = Colors()
    static let fonts = Fonts()
    static let spacing = Spacing()
    static let cornerRadius: CGFloat = 12
    static let shadowRadius: CGFloat = 4
}

struct Colors {
    let primary = Color.blue
    let secondary = Color.purple
    let accent = Color.orange
    let background = Color(UIColor.systemBackground)
    let secondaryBackground = Color(UIColor.secondarySystemBackground)
    let text = Color(UIColor.label)
    let secondaryText = Color(UIColor.secondaryLabel)
    
    func forCategory(_ category: CourseCategory) -> Color {
        switch category {
        case .core:
            return .blue
        case .aiResearch:
            return .purple
        case .specialized:
            return .orange
        case .industryAndEthics:
            return .green
        }
    }
    
    func forDifficulty(_ difficulty: CourseDifficulty) -> Color {
        switch difficulty {
        case .beginner:
            return .green
        case .intermediate:
            return .orange
        case .advanced:
            return .red
        }
    }
}

struct Fonts {
    let title = Font.system(.title, design: .rounded).weight(.bold)
    let title2 = Font.system(.title2, design: .rounded).weight(.semibold)
    let title3 = Font.system(.title3, design: .rounded).weight(.semibold)
    let headline = Font.system(.headline, design: .rounded)
    let body = Font.system(.body, design: .rounded)
    let caption = Font.system(.caption, design: .rounded)
}

struct Spacing {
    let small: CGFloat = 8
    let medium: CGFloat = 16
    let large: CGFloat = 24
    let extraLarge: CGFloat = 32
}

// MARK: - View Modifiers
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(Theme.spacing.medium)
            .background(Theme.colors.secondaryBackground)
            .cornerRadius(Theme.cornerRadius)
            .shadow(radius: Theme.shadowRadius)
    }
}

struct PillModifier: ViewModifier {
    let color: Color
    
    func body(content: Content) -> some View {
        content
            .padding(.horizontal, Theme.spacing.medium)
            .padding(.vertical, Theme.spacing.small)
            .background(color.opacity(0.2))
            .foregroundColor(color)
            .cornerRadius(20)
    }
}

// MARK: - View Extensions
extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
    
    func pillStyle(color: Color) -> some View {
        modifier(PillModifier(color: color))
    }
} 