#!/usr/bin/env python3

# Read the current admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the showTab function to properly handle the event
old_function = """function showTab(tabName) {
            // Alle Tabs deaktivieren
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Aktiven Tab aktivieren
            event.target.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');
            
            // Spezifische Daten laden
            if (tabName === 'preferences') {
                loadPreferences();
            }
        }"""

new_function = """function showTab(tabName) {
            // Alle Tabs deaktivieren
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Aktiven Tab aktivieren
            // Find the button that was clicked based on the tabName
            document.querySelectorAll('.tab').forEach(tab => {
                if (tab.onclick && tab.onclick.toString().includes("'" + tabName + "'")) {
                    tab.classList.add('active');
                }
            });
            
            // Show the content
            const tabContent = document.getElementById('tab-' + tabName);
            if (tabContent) {
                tabContent.classList.add('active');
            }
            
            // Spezifische Daten laden
            if (tabName === 'preferences') {
                loadPreferences();
            }
            
            // Update participant count when email tab is shown
            if (tabName === 'email') {
                updateParticipantCount();
            }
        }"""

# Replace the function
content = content.replace(old_function, new_function)

# Save the file
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ showTab Funktion gefixt")
