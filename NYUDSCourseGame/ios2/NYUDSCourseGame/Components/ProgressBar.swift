import SwiftUI

struct ProgressBar: View {
    let progress: Double
    let color: Color
    let height: CGFloat
    
    init(progress: Double, color: Color = Theme.colors.primary, height: CGFloat = 8) {
        self.progress = min(max(progress, 0), 1)
        self.color = color
        self.height = height
    }
    
    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                Rectangle()
                    .frame(width: geometry.size.width, height: height)
                    .opacity(0.3)
                    .foregroundColor(color)
                
                Rectangle()
                    .frame(width: min(CGFloat(progress) * geometry.size.width, geometry.size.width), height: height)
                    .foregroundColor(color)
            }
            .cornerRadius(height / 2)
        }
        .frame(height: height)
    }
}

struct AnimatedProgressBar: View {
    let progress: Double
    let color: Color
    let height: CGFloat
    @State private var animatedProgress: Double = 0
    
    init(progress: Double, color: Color = Theme.colors.primary, height: CGFloat = 8) {
        self.progress = min(max(progress, 0), 1)
        self.color = color
        self.height = height
    }
    
    var body: some View {
        ProgressBar(progress: animatedProgress, color: color, height: height)
            .onAppear {
                withAnimation(.easeInOut(duration: 1.0)) {
                    animatedProgress = progress
                }
            }
            .onChange(of: progress) { newValue in
                withAnimation(.easeInOut(duration: 1.0)) {
                    animatedProgress = newValue
                }
            }
    }
}

// MARK: - Preview
struct ProgressBar_Previews: PreviewProvider {
    static var previews: some View {
        VStack(spacing: Theme.spacing.large) {
            ProgressBar(progress: 0.3)
            ProgressBar(progress: 0.7, color: .green)
            AnimatedProgressBar(progress: 0.5, color: .purple)
        }
        .padding()
    }
} 