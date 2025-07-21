#!/usr/bin/env python3
import re

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML-Header erweitern: neue Spalte nach "Begleitung"
header_pattern = r'(<th>Begleitung</th>)\s*\n\s*(<th>Anmeldedatum</th>)'
header_replacement = r'\1\n                                <th>Gesamt-Personen</th>\n                                \2'
content = re.sub(header_pattern, header_replacement, content)

# 2. Loading-Message colspan von 5 auf 6 ändern
colspan_pattern = r'<td colspan="5" class="loading">Lade Teilnehmer...</td>'
colspan_replacement = '<td colspan="6" class="loading">Lade Teilnehmer...</td>'
content = content.replace(colspan_pattern, colspan_replacement)

# 3. "Noch keine Anmeldungen" colspan von 5 auf 6 ändern
no_participants_pattern = r'<td colspan="5" style="text-align: center; color: #666;">Noch keine Anmeldungen</td>'
no_participants_replacement = '<td colspan="6" style="text-align: center; color: #666;">Noch keine Anmeldungen</td>'
content = content.replace(no_participants_pattern, no_participants_replacement)

# 4. updateParticipantsTable() erweitern
table_update_pattern = r'(\s+<td>\$\{companions\}</td>)\s*\n(\s+<td>\$\{formattedDate\}</td>)'
table_update_replacement = r'\1\n                        <td style="text-align: center; font-weight: bold;">${calculateTotalPersons(p)}</td>\n\2'
content = re.sub(table_update_pattern, table_update_replacement, content)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Gesamtpersonen-Spalte erfolgreich hinzugefügt!")
