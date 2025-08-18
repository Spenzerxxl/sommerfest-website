#!/usr/bin/env python3
import re

# Lese die fehlerhafte admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Finde die Position des E-Mail-Tabs
email_tab_start = content.find('<!-- Tab: E-Mail Versand -->')
email_tab_end = content.find('<!-- Logen-Übersicht -->')

if email_tab_start == -1 or email_tab_end == -1:
    print("Konnte Tab-Positionen nicht finden!")
    exit(1)

# Extrahiere die Teile
before_email = content[:email_tab_start].rstrip()
email_tab = content[email_tab_start:email_tab_end].rstrip()
after_email = content[email_tab_end:]

# Füge den E-Mail-Tab nach dem Export-Tab ein, aber vor der Logen-Übersicht
# Der Export-Tab endet mit </div> (2x), dann kommt der E-Mail-Tab
fixed_content = before_email + '\n            </div>\n            ' + email_tab + '\n            </div>\n            ' + after_email

# Schreibe die korrigierte Version
with open('admin.html.fixed', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Struktur korrigiert und in admin.html.fixed gespeichert")
