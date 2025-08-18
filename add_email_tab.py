#!/usr/bin/env python3
import re

# Read the current admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the email button emoji
content = content.replace('ud83dudce7 E-Mail Versand', '📧 E-Mail Versand')

# Find where to insert the email tab content (after the last tab-content div)
# Look for the closing of tab-export
export_tab_pattern = r'(<div id="tab-export"[^>]*>.*?</div>\s*</div>)'
match = re.search(export_tab_pattern, content, re.DOTALL)

if match:
    insert_position = match.end()
    
    # Email tab content to insert
    email_tab_content = '''
            <!-- Tab: E-Mail Versand -->
            <div id="tab-email" class="tab-content">
                <h3>📧 E-Mail Reminder versenden</h3>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #17a2b8;">
                    <p style="font-size: 16px; margin-bottom: 10px;">📊 Sendet personalisierte Erinnerungen an alle <span id="participantCount" style="font-weight: bold; color: #2a5298;">-</span> Teilnehmer:</p>
                    <ul style="margin-left: 20px; color: #6c757d;">
                        <li style="margin: 5px 0;">Normale Teilnehmer → Allgemeine Erinnerung</li>
                        <li style="margin: 5px 0;">Aufbau-Helfer → Erinnerung + Aufbau-Info (22.08., 16:00)</li>
                        <li style="margin: 5px 0;">Abbau-Helfer → Erinnerung + Abbau-Info (24.08., 14:00)</li>
                        <li style="margin: 5px 0;">Aufbau+Abbau → Erinnerung + beide Termine</li>
                    </ul>
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 20px; margin-top: 30px; max-width: 600px;">
                    <button onclick="sendSmartReminder()" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; border: none; padding: 20px 30px; border-radius: 10px; cursor: pointer; font-size: 18px; font-weight: bold; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);">
                        🚀 Intelligente Reminder versenden
                        <small style="display: block; font-weight: normal; font-size: 14px; margin-top: 5px; opacity: 0.9;">Jeder Teilnehmer erhält die passende E-Mail-Variante</small>
                    </button>
                </div>
                
                <div id="emailStatus" style="margin-top: 20px; padding: 15px; border-radius: 5px; display: none;"></div>
            </div>
'''
    
    # Insert the email tab content
    content = content[:insert_position] + email_tab_content + content[insert_position:]
    
    print("✅ E-Mail Tab Content hinzugefügt")
else:
    print("❌ Konnte Position für E-Mail Tab nicht finden")

# Save the modified file
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Datei gespeichert")
