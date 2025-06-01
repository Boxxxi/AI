import SwiftUI

struct ConfettiView: View {
    @State private var isAnimating = false
    let colors: [Color]
    
    init(colors: [Color] = [.red, .blue, .green, .yellow, .purple, .orange]) {
        self.colors = colors
    }
    
    var body: some View {
        ZStack {
            ForEach(0..<50) { index in
                ConfettiPiece(index: index, colors: colors)
                    .opacity(isAnimating ? 1 : 0)
            }
        }
        .onAppear {
            withAnimation(.easeOut(duration: 2.0)) {
                isAnimating = true
            }
        }
    }
}

struct ConfettiPiece: View {
    let index: Int
    let colors: [Color]
    @State private var position: CGPoint = .zero
    @State private var rotation: Double = 0
    @State private var scale: CGFloat = 1
    
    var body: some View {
        Circle()
            .fill(colors[index % colors.count])
            .frame(width: 8, height: 8)
            .position(position)
            .rotationEffect(.degrees(rotation))
            .scaleEffect(scale)
            .onAppear {
                let randomX = CGFloat.random(in: 0...UIScreen.main.bounds.width)
                let randomY = CGFloat.random(in: -UIScreen.main.bounds.height...0)
                position = CGPoint(x: randomX, y: randomY)
                
                withAnimation(.easeOut(duration: Double.random(in: 1.0...2.0))) {
                    position.y = UIScreen.main.bounds.height + 100
                    rotation = Double.random(in: 0...360)
                    scale = CGFloat.random(in: 0.5...1.5)
                }
            }
    }
}

struct CelebrationView: View {
    let title: String
    let message: String
    let icon: String
    let xpEarned: Int
    @State private var showConfetti = false
    
    var body: some View {
        ZStack {
            VStack(spacing: Theme.spacing.large) {
                Image(systemName: icon)
                    .font(.system(size: 60))
                    .foregroundColor(Theme.colors.accent)
                
                Text(title)
                    .font(Theme.fonts.title)
                    .multilineTextAlignment(.center)
                
                Text(message)
                    .font(Theme.fonts.body)
                    .multilineTextAlignment(.center)
                
                HStack {
                    Image(systemName: "star.fill")
                        .foregroundColor(.yellow)
                    Text("+\(xpEarned) XP")
                        .font(Theme.fonts.title3)
                }
                .padding()
                .background(Theme.colors.secondaryBackground)
                .cornerRadius(Theme.cornerRadius)
            }
            .padding()
            .background(Theme.colors.background)
            .cornerRadius(Theme.cornerRadius)
            .shadow(radius: Theme.shadowRadius)
            
            if showConfetti {
                ConfettiView()
                    .allowsHitTesting(false)
            }
        }
        .onAppear {
            withAnimation(.easeIn(duration: 0.5)) {
                showConfetti = true
            }
        }
    }
}

// MARK: - Preview
struct ConfettiView_Previews: PreviewProvider {
    static var previews: some View {
        CelebrationView(
            title: "Course Completed!",
            message: "You've mastered all flashcards in Introduction to Data Science",
            icon: "graduationcap.fill",
            xpEarned: 500
        )
        .padding()
    }
} 