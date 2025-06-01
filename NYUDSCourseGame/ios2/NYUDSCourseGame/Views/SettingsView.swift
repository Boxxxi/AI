import SwiftUI

struct SettingsView: View {
    @ObservedObject private var settings = SettingsManager.shared
    @State private var showingResetConfirmation = false
    
    var body: some View {
        NavigationView {
            Form {
                // Sound & Haptics Section
                Section(header: Text("Sound & Haptics")) {
                    Toggle("Sound Effects", isOn: $settings.soundEnabled)
                    Toggle("Haptic Feedback", isOn: $settings.hapticsEnabled)
                }
                
                // Appearance Section
                Section(header: Text("Appearance")) {
                    Toggle("Dark Mode", isOn: $settings.darkModeEnabled)
                }
                
                // Notifications Section
                Section(header: Text("Notifications")) {
                    Toggle("Daily Reminders", isOn: $settings.notificationsEnabled)
                        .onChange(of: settings.notificationsEnabled) { newValue in
                            if newValue {
                                settings.requestNotificationPermission()
                            }
                        }
                    
                    if settings.notificationsEnabled {
                        DatePicker("Reminder Time", selection: $settings.dailyReminderTime, displayedComponents: .hourAndMinute)
                    }
                }
                
                // Reset Section
                Section {
                    Button(action: {
                        showingResetConfirmation = true
                    }) {
                        HStack {
                            Image(systemName: "arrow.counterclockwise")
                            Text("Reset All Settings")
                        }
                        .foregroundColor(.red)
                    }
                }
            }
            .navigationTitle("Settings")
            .alert(isPresented: $showingResetConfirmation) {
                Alert(
                    title: Text("Reset Settings"),
                    message: Text("Are you sure you want to reset all settings to their default values?"),
                    primaryButton: .destructive(Text("Reset")) {
                        settings.resetAllSettings()
                    },
                    secondaryButton: .cancel()
                )
            }
        }
    }
}

// MARK: - Preview
struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
} 