#!/usr/bin/env python3
import re

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# CSS für die neue Gesamt-Personen-Spalte hinzufügen
css_addition = '''        /* Gesamt-Personen-Spalte Styling */
        table th:nth-child(5) { 
            width: 120px; 
            text-align: center; 
            background-color: #e8f5e8; 
        }
        table td:nth-child(5) { 
            width: 120px; 
            text-align: center; 
            font-weight: bold; 
            color: #2c5530; 
            background-color: #f0f8f0; 
        }

'''

# Finde die Stelle im CSS-Bereich und füge das CSS hinzu
css_pattern = r'(        \.logout-btn:hover \{[^}]+\})\s*\n(\s*</style>)'
css_replacement = r'\1\n\n' + css_addition + r'        \2'

content = re.sub(css_pattern, css_replacement, content, flags=re.DOTALL)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSS-Styling für Gesamt-Personen-Spalte hinzugefügt!")
