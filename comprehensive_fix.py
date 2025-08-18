#!/usr/bin/env python3
import re

# Read the current admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Simplify showTab function
old_showtab = """function showTab(tabName) {
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

new_showtab = """function showTab(tabName) {
            console.log('Switching to tab:', tabName);
            
            // Alle Tabs deaktivieren
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => {
                c.classList.remove('active');
                c.style.display = 'none';
            });
            
            // Finde und aktiviere den Button
            document.querySelectorAll('.tab').forEach(button => {
                const onclickStr = button.getAttribute('onclick');
                if (onclickStr && onclickStr.includes("'" + tabName + "'")) {
                    button.classList.add('active');
                    console.log('Activated button for:', tabName);
                }
            });
            
            // Zeige den Content
            const tabContent = document.getElementById('tab-' + tabName);
            if (tabContent) {
                tabContent.classList.add('active');
                tabContent.style.display = 'block';
                console.log('Showing content for:', tabName);
            } else {
                console.error('Tab content not found for:', tabName);
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
content = content.replace(old_showtab, new_showtab)

# Fix 2: Make sure the initial tab is visible
content = content.replace(
    '<div id="tab-participants" class="tab-content active">',
    '<div id="tab-participants" class="tab-content active" style="display: block;">'
)

# Save the file
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Comprehensive fix applied")
