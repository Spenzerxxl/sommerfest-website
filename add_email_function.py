#!/usr/bin/env python3
import re

# Read the current admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the function (before the closing </script> tag)
script_end_pattern = r'(</script>)'
match = re.search(script_end_pattern, content)

if match:
    insert_position = match.start()
    
    # Email function to insert
    email_function = '''
        // E-Mail Reminder Function
        async function sendSmartReminder() {
            // Admin check
            if (!isLoggedIn) {
                alert('Nicht autorisiert! Bitte melden Sie sich an.');
                return;
            }
            
            // Get current participant count
            const participantCount = currentData.participants ? currentData.participants.length : 0;
            
            if (participantCount === 0) {
                alert('Keine Teilnehmer gefunden!');
                return;
            }
            
            // Security confirmation
            if (!confirm(`Wirklich personalisierte E-Mails an alle ${participantCount} Teilnehmer versenden?\\n\\nJeder erhält automatisch die passende Variante:\\n- Normale Teilnehmer: Nur Fest-Erinnerung\\n- Aufbau-Helfer: + Aufbau-Info (22.08., 16:00)\\n- Abbau-Helfer: + Abbau-Info (24.08., 14:00)\\n- Beide: + beide Termine`)) {
                return;
            }
            
            const statusDiv = document.getElementById('emailStatus');
            statusDiv.style.display = 'block';
            statusDiv.style.background = '#d1ecf1';
            statusDiv.style.color = '#0c5460';
            statusDiv.style.borderLeft = '4px solid #17a2b8';
            
            try {
                statusDiv.innerHTML = '⏳ E-Mails werden vorbereitet...';
                
                const response = await fetch('https://automatisierung.frankrath.de/webhook/send-smart-reminder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        participants: currentData.participants
                    })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    statusDiv.style.background = '#d4edda';
                    statusDiv.style.color = '#155724';
                    statusDiv.style.borderLeft = '4px solid #28a745';
                    statusDiv.innerHTML = `✅ Personalisierte E-Mails wurden an ${participantCount} Teilnehmer versendet!<br><small>Die Versendung läuft im Hintergrund und kann einige Minuten dauern.</small>`;
                } else {
                    throw new Error('Server-Fehler');
                }
            } catch (error) {
                console.error('Error sending reminder:', error);
                statusDiv.style.background = '#f8d7da';
                statusDiv.style.color = '#721c24';
                statusDiv.style.borderLeft = '4px solid #dc3545';
                statusDiv.innerHTML = '❌ Fehler beim Versand! Bitte prüfen Sie die n8n-Workflows.';
            }
        }
        
        // Update participant count in email tab
        function updateParticipantCount() {
            const countElement = document.getElementById('participantCount');
            if (countElement && currentData.participants) {
                countElement.textContent = currentData.participants.length;
            }
        }
    '''
    
    # Insert the function
    content = content[:insert_position] + email_function + '\n    ' + content[insert_position:]
    
    # Also update the loadDashboardData function to call updateParticipantCount
    content = content.replace(
        'updateExtendedPreferencesDisplay();',
        'updateExtendedPreferencesDisplay();\n                    updateParticipantCount();'
    )
    
    print("✅ JavaScript-Funktion hinzugefügt")
else:
    print("❌ Konnte Position für JavaScript nicht finden")

# Save the modified file
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Datei gespeichert")
