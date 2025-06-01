import Foundation
import Combine

class SettingsManager: ObservableObject {
    static let shared = SettingsManager()
    
    @Published var soundEnabled: Bool {
        didSet {
            UserDefaults.standard.set(soundEnabled, forKey: "soundEnabled")
        }
    }
    
    @Published var hapticsEnabled: Bool {
        didSet {
            UserDefaults.standard.set(hapticsEnabled, forKey: "hapticsEnabled")
        }
    }
    
    @Published var darkModeEnabled: Bool {
        didSet {
            UserDefaults.standard.set(darkModeEnabled, forKey: "darkModeEnabled")
        }
    }
    
    @Published var notificationsEnabled: Bool {
        didSet {
            UserDefaults.standard.set(notificationsEnabled, forKey: "notificationsEnabled")
        }
    }
    
    @Published var dailyReminderTime: Date {
        didSet {
            UserDefaults.standard.set(dailyReminderTime, forKey: "dailyReminderTime")
            scheduleDailyReminder()
        }
    }
    
    private init() {
        // Load settings from UserDefaults
        soundEnabled = UserDefaults.standard.bool(forKey: "soundEnabled")
        hapticsEnabled = UserDefaults.standard.bool(forKey: "hapticsEnabled")
        darkModeEnabled = UserDefaults.standard.bool(forKey: "darkModeEnabled")
        notificationsEnabled = UserDefaults.standard.bool(forKey: "notificationsEnabled")
        
        if let savedTime = UserDefaults.standard.object(forKey: "dailyReminderTime") as? Date {
            dailyReminderTime = savedTime
        } else {
            // Default to 8:00 AM
            var components = DateComponents()
            components.hour = 8
            components.minute = 0
            dailyReminderTime = Calendar.current.date(from: components) ?? Date()
        }
    }
    
    private func scheduleDailyReminder() {
        guard notificationsEnabled else { return }
        
        let content = UNMutableNotificationContent()
        content.title = "Time to Study!"
        content.body = "Don't break your streak! Study some flashcards today."
        content.sound = .default
        
        let calendar = Calendar.current
        let components = calendar.dateComponents([.hour, .minute], from: dailyReminderTime)
        
        let trigger = UNCalendarNotificationTrigger(
            dateMatching: components,
            repeats: true
        )
        
        let request = UNNotificationRequest(
            identifier: "dailyReminder",
            content: content,
            trigger: trigger
        )
        
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                print("Failed to schedule daily reminder: \(error)")
            }
        }
    }
    
    func requestNotificationPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                self.notificationsEnabled = true
            } else if let error = error {
                print("Failed to request notification permission: \(error)")
            }
        }
    }
    
    func resetAllSettings() {
        soundEnabled = true
        hapticsEnabled = true
        darkModeEnabled = false
        notificationsEnabled = false
        
        var components = DateComponents()
        components.hour = 8
        components.minute = 0
        dailyReminderTime = Calendar.current.date(from: components) ?? Date()
    }
} 