import SwiftUI

struct StreakView: View {
    let streak: Int
    let size: CGFloat
    
    init(streak: Int, size: CGFloat = 40) {
        self.streak = streak
        self.size = size
    }
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: "flame.fill")
                .font(.system(size: size * 0.8))
                .foregroundColor(.orange)
            
            Text("\(streak)")
                .font(.system(size: size, weight: .bold, design: .rounded))
                .foregroundColor(.orange)
            
            Text("days")
                .font(.system(size: size * 0.4, weight: .medium, design: .rounded))
                .foregroundColor(.secondary)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.orange.opacity(0.1))
        )
    }
}

struct StreakCalendarView: View {
    let streak: Int
    let lastStudyDate: Date?
    
    private var calendar = Calendar.current
    private var today = Date()
    
    private var lastWeek: [Date] {
        let days = (0...6).map { calendar.date(byAdding: .day, value: -$0, to: today)! }
        return days.reversed()
    }
    
    private func isStudiedOn(_ date: Date) -> Bool {
        guard let lastStudy = lastStudyDate else { return false }
        return calendar.isDate(date, inSameDayAs: lastStudy)
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Study Streak")
                .font(Theme.fonts.headline)
            
            HStack(spacing: 4) {
                ForEach(lastWeek, id: \.self) { date in
                    VStack(spacing: 4) {
                        Text(calendar.veryShortWeekdaySymbols[calendar.component(.weekday, from: date) - 1])
                            .font(.caption2)
                            .foregroundColor(.secondary)
                        
                        Circle()
                            .fill(isStudiedOn(date) ? Color.orange : Color.gray.opacity(0.2))
                            .frame(width: 24, height: 24)
                            .overlay(
                                Text("\(calendar.component(.day, from: date))")
                                    .font(.caption2)
                                    .foregroundColor(isStudiedOn(date) ? .white : .secondary)
                            )
                    }
                }
            }
        }
        .padding()
        .background(Theme.colors.secondaryBackground)
        .cornerRadius(Theme.cornerRadius)
    }
}

// MARK: - Preview
struct StreakView_Previews: PreviewProvider {
    static var previews: some View {
        VStack(spacing: Theme.spacing.large) {
            StreakView(streak: 7)
            StreakCalendarView(streak: 3, lastStudyDate: Date())
        }
        .padding()
    }
} 