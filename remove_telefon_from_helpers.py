#!/usr/bin/env python3
import re

print("🔧 Entferne Telefon aus Helfer-Export-Datenstruktur...")

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Telefon-Zeile aus Helfer-Export entfernen
old_helper_structure = '''            ).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));'''

new_helper_structure = '''            ).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));'''

content = content.replace(old_helper_structure, new_helper_structure)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Telefon-Referenz aus Helfer-Export entfernt!")
