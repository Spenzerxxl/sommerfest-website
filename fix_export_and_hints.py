#!/usr/bin/env python3
import re

print("🔧 Starte Export- und Hinweise-Reparaturen...")

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. UTF-8 BOM zu CSV-Export hinzufügen (löst "kauderwelsch" Problem)
print("1️⃣ Füge UTF-8 BOM zu CSV-Export hinzu...")

export_function_old = '''function exportToCSV(data, filename) {
            const csv = convertToCSV(data);
            const blob = new Blob([csv], { type: 'text/csv' });'''

export_function_new = '''function exportToCSV(data, filename) {
            const csv = convertToCSV(data);
            // UTF-8 BOM hinzufügen für korrekte deutsche Umlaute
            const csvWithBOM = '\\ufeff' + csv;
            const blob = new Blob([csvWithBOM], { type: 'text/csv;charset=utf-8;' });'''

content = content.replace(export_function_old, export_function_new)

# 2. Hinweise-Spalte zur Teilnehmer-Tabelle hinzufügen
print("2️⃣ Füge Hinweise-Spalte zu Teilnehmer-Tabelle hinzu...")

# HTML-Header erweitern
participants_header_old = '''                                <th>Gesamt-Personen</th>
                                <th>Anmeldedatum</th>'''

participants_header_new = '''                                <th>Gesamt-Personen</th>
                                <th>Anmeldedatum</th>
                                <th>Hinweise</th>'''

content = content.replace(participants_header_old, participants_header_new)

# Loading message colspan von 6 auf 7
content = content.replace(
    '<td colspan="6" class="loading">Lade Teilnehmer...</td>',
    '<td colspan="7" class="loading">Lade Teilnehmer...</td>'
)

# "Noch keine Anmeldungen" colspan von 6 auf 7
content = content.replace(
    '<td colspan="6" style="text-align: center; color: #666;">Noch keine Anmeldungen</td>',
    '<td colspan="7" style="text-align: center; color: #666;">Noch keine Anmeldungen</td>'
)

# updateParticipantsTable() Function erweitern
participants_table_old = '''                        <td style="text-align: center; font-weight: bold;">${calculateTotalPersons(p)}</td>
                        <td>${formattedDate}</td>
                    </tr>'''

participants_table_new = '''                        <td style="text-align: center; font-weight: bold;">${calculateTotalPersons(p)}</td>
                        <td>${formattedDate}</td>
                        <td>${p.bemerkungen || 'Keine Hinweise'}</td>
                    </tr>'''

content = content.replace(participants_table_old, participants_table_new)

# 3. Fehlende Export-Event-Listener hinzufügen
print("3️⃣ Füge fehlende Export-Event-Listener hinzu...")

# Position nach dem letzten Event-Listener finden
event_listener_insertion_point = '''        document.getElementById('exportPreferences').addEventListener('click', function() {
            const prefData = currentData.participants.map(p => ({
                name: p.name,
                email: p.email,
                grillbuffet_praeferenzen: p.grillbuffet_praeferenzen || '',
                grillbuffet_bemerkungen: p.grillbuffet_bemerkungen || '',
                getraenke_praeferenzen: p.getraenke_praeferenzen || '',
                getraenke_bemerkungen: p.getraenke_bemerkungen || ''
            }));
            exportToCSV(prefData, 'sommerfest_praeferenzen.csv');
        });'''

# Neue Event-Listener hinzufügen
new_event_listeners = '''        document.getElementById('exportPreferences').addEventListener('click', function() {
            const prefData = currentData.participants.map(p => ({
                name: p.name,
                email: p.email,
                grillbuffet_praeferenzen: p.grillbuffet_praeferenzen || '',
                grillbuffet_bemerkungen: p.grillbuffet_bemerkungen || '',
                getraenke_praeferenzen: p.getraenke_praeferenzen || '',
                getraenke_bemerkungen: p.getraenke_bemerkungen || ''
            }));
            exportToCSV(prefData, 'sommerfest_praeferenzen.csv');
        });

        // NEUE: Export-Buffet-Planung
        document.getElementById('exportBuffet').addEventListener('click', function() {
            const buffetItems = [];
            currentData.participants.forEach(p => {
                if (p.buffet) {
                    try {
                        const buffetData = JSON.parse(p.buffet);
                        buffetData.forEach(item => {
                            buffetItems.push({
                                gericht: item.item || item.name,
                                anbieter: p.name,
                                portionen: item.quantity,
                                email: p.email,
                                telefon: p.telefon || 'Nicht angegeben'
                            });
                        });
                    } catch (e) {
                        if (p.buffet.trim()) {
                            buffetItems.push({
                                gericht: p.buffet,
                                anbieter: p.name,
                                portionen: p.quantity || 'Nicht angegeben',
                                email: p.email,
                                telefon: p.telefon || 'Nicht angegeben'
                            });
                        }
                    }
                }
            });
            exportToCSV(buffetItems, 'sommerfest_buffet_planung.csv');
        });

        // NEUE: Export-Helfer-Liste
        document.getElementById('exportHelpers').addEventListener('click', function() {
            const helperData = currentData.participants.map(p => ({
                name: p.name,
                email: p.email,
                telefon: p.telefon || '',
                aufbau: p.helfer_aufbau || '',
                abbau: p.helfer_abbau || '',
                hinweise: p.bemerkungen || ''
            })).filter(h => h.aufbau || h.abbau); // Nur echte Helfer
            exportToCSV(helperData, 'sommerfest_helfer_liste.csv');
        });'''

content = content.replace(event_listener_insertion_point, new_event_listeners)

# 4. CSS für neue Hinweise-Spalte hinzufügen
print("4️⃣ Erweitere CSS für Hinweise-Spalte...")

css_addition = '''
        /* Hinweise-Spalte in Teilnehmer-Tabelle */
        table th:nth-child(7) { 
            width: 150px; 
            text-align: left; 
            background-color: #fff3cd; 
        }
        table td:nth-child(7) { 
            width: 150px; 
            font-size: 12px; 
            color: #856404; 
            background-color: #fefefe; 
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
'''

# CSS vor </style> einfügen
css_pattern = r'(\s+)(</style>)'
css_replacement = r'\1' + css_addition + r'\n        \2'
content = re.sub(css_pattern, css_replacement, content)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Alle Reparaturen abgeschlossen!")
print("   → UTF-8 BOM für CSV-Export hinzugefügt")
print("   → Hinweise-Spalte zu Teilnehmer-Tabelle verschoben")
print("   → Export-Buttons für Buffet und Helfer implementiert")
print("   → CSS-Styling erweitert")
