import SwiftUI
import Combine

class NotificationManager: ObservableObject {
    @Published var currentNotification: NotificationItem?
    private var notificationQueue: [NotificationItem] = []
    private var timer: Timer?
    
    static let shared = NotificationManager()
    
    private init() {}
    
    func showNotification(_ notification: NotificationItem) {
        if currentNotification == nil {
            currentNotification = notification
            startTimer()
        } else {
            notificationQueue.append(notification)
        }
    }
    
    private func startTimer() {
        timer?.invalidate()
        timer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: false) { [weak self] _ in
            self?.dismissCurrentNotification()
        }
    }
    
    private func dismissCurrentNotification() {
        withAnimation {
            currentNotification = nil
        }
        
        if !notificationQueue.isEmpty {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) { [weak self] in
                self?.currentNotification = self?.notificationQueue.removeFirst()
                self?.startTimer()
            }
        }
    }
}

struct NotificationItem: Identifiable {
    let id = UUID()
    let title: String
    let message: String
    let type: NotificationType
    let icon: String
    let action: (() -> Void)?
    
    init(title: String, message: String, type: NotificationType, icon: String, action: (() -> Void)? = nil) {
        self.title = title
        self.message = message
        self.type = type
        self.icon = icon
        self.action = action
    }
}

enum NotificationType {
    case success
    case info
    case warning
    case achievement
    
    var color: Color {
        switch self {
        case .success: return .green
        case .info: return .blue
        case .warning: return .orange
        case .achievement: return .purple
        }
    }
}

struct NotificationView: View {
    let notification: NotificationItem
    
    var body: some View {
        HStack(spacing: Theme.spacing.medium) {
            Image(systemName: notification.icon)
                .font(.title2)
                .foregroundColor(notification.type.color)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(notification.title)
                    .font(Theme.fonts.headline)
                
                Text(notification.message)
                    .font(Theme.fonts.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            if notification.action != nil {
                Button(action: {
                    notification.action?()
                }) {
                    Image(systemName: "chevron.right")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(Theme.colors.background)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: Theme.shadowRadius)
        .padding(.horizontal)
    }
}

struct NotificationContainerView: View {
    @ObservedObject private var manager = NotificationManager.shared
    
    var body: some View {
        ZStack {
            if let notification = manager.currentNotification {
                VStack {
                    NotificationView(notification: notification)
                        .transition(.move(edge: .top).combined(with: .opacity))
                    Spacer()
                }
                .animation(.spring(), value: notification)
            }
        }
    }
}

// MARK: - Preview
struct NotificationView_Previews: PreviewProvider {
    static var previews: some View {
        VStack(spacing: Theme.spacing.medium) {
            NotificationView(
                notification: NotificationItem(
                    title: "Course Completed!",
                    message: "You've mastered Introduction to Data Science",
                    type: .success,
                    icon: "checkmark.circle.fill"
                )
            )
            
            NotificationView(
                notification: NotificationItem(
                    title: "New Achievement!",
                    message: "Mastered 100 flashcards",
                    type: .achievement,
                    icon: "star.fill"
                )
            )
        }
        .padding()
    }
} 