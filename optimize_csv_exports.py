#!/usr/bin/env python3
import re

print("🔧 Optimiere CSV-Exports: Überflüssige Spalten entfernen + Abrechnungs-Export...")

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Teilnehmerliste-Export: Überflüssige Spalten entfernen
print("1️⃣ Entferne überflüssige Spalten aus Teilnehmerliste...")

old_participant_data = '''                return {
                    'Name': p.name || 'N/A',
                    'E-Mail': p.email || 'N/A',
                    'Telefon': p.telefon || 'Nicht angegeben',
                    'Loge': lodge,
                    'Begleitung': guests,
                    'Gesamt-Personen': totalPersons,
                    'Anmeldedatum': formattedDate,
                    'Buffet-Beiträge': buffetItems,
                    'Aufbau-Helfer': p.helfer_aufbau || 'Nein',
                    'Abbau-Helfer': p.helfer_abbau || 'Nein',
                    'Hinweise': p.bemerkungen || 'Keine',
                    'Grillbuffet-Präferenzen': p.grillbuffet_praeferenzen || 'Keine Angabe',
                    'Getränke-Präferenzen': p.getraenke_praeferenzen || 'Keine Angabe'
                };'''

new_participant_data = '''                return {
                    'Name': p.name || 'N/A',
                    'E-Mail': p.email || 'N/A',
                    'Loge': lodge,
                    'Begleitung': guests,
                    'Gesamt-Personen': totalPersons,
                    'Anmeldedatum': formattedDate,
                    'Buffet-Beiträge': buffetItems,
                    'Aufbau-Helfer': p.helfer_aufbau || 'Nein',
                    'Abbau-Helfer': p.helfer_abbau || 'Nein',
                    'Hinweise': p.bemerkungen || 'Keine'
                };'''

content = content.replace(old_participant_data, new_participant_data)

# Headers für Teilnehmerliste anpassen
old_headers = "const headers = ['Name', 'E-Mail', 'Telefon', 'Loge', 'Begleitung', 'Gesamt-Personen', 'Anmeldedatum', 'Buffet-Beiträge', 'Aufbau-Helfer', 'Abbau-Helfer', 'Hinweise', 'Grillbuffet-Präferenzen', 'Getränke-Präferenzen'];"

new_headers = "const headers = ['Name', 'E-Mail', 'Loge', 'Begleitung', 'Gesamt-Personen', 'Anmeldedatum', 'Buffet-Beiträge', 'Aufbau-Helfer', 'Abbau-Helfer', 'Hinweise'];"

content = content.replace(old_headers, new_headers)

# 2. Neuen Export-Button "Abrechnung" hinzufügen
print("2️⃣ Füge neuen Export-Button 'Abrechnung' hinzu...")

old_export_buttons = '''                        <button class="btn btn-primary" id="exportHelpers">
                            🤝 Helfer-Liste
                        </button>
                    </div>'''

new_export_buttons = '''                        <button class="btn btn-primary" id="exportHelpers">
                            🤝 Helfer-Liste
                        </button>
                        <button class="btn btn-warning" id="exportBilling" style="background-color: #f39c12;">
                            💰 Abrechnung (für Kasse)
                        </button>
                    </div>'''

content = content.replace(old_export_buttons, new_export_buttons)

# 3. Event-Listener für Abrechnungs-Export hinzufügen
print("3️⃣ Implementiere Abrechnungs-Export-Funktion...")

# Nach dem exportHelpers Event-Listener einfügen
helpers_listener_end = '''            exportToCSV(helperData, headers, 'sommerfest_helfer_liste.csv');
        });'''

billing_listener = '''            exportToCSV(helperData, headers, 'sommerfest_helfer_liste.csv');
        });

        document.getElementById('exportBilling').addEventListener('click', function() {
            console.log('Export Abrechnung gestartet...');
            
            const billingData = currentData.participants.map(p => {
                // Lodge-Mapping anwenden
                const lodge = mapLodgeFromData(p.email, p.name);
                
                // Gäste-Korrektur anwenden  
                const correctedData = correctGuestDataFromPattern(p);
                const guests = correctedData ? correctedData.gaeste : (p.gaeste || 'Keine');
                const totalPersons = correctedData ? correctedData.personen : (parseInt(p.personen) || 1);
                
                return {
                    'Name': p.name || 'N/A',
                    'Loge': lodge,
                    'Begleitung': guests,
                    'Gesamtpersonen': totalPersons,
                    'Bezahlt': ''  // Leere Spalte zum handschriftlichen Eintragen
                };
            });
            
            const headers = ['Name', 'Loge', 'Begleitung', 'Gesamtpersonen', 'Bezahlt'];
            
            exportToCSV(billingData, headers, 'sommerfest_abrechnung_kasse.csv');
        });'''

content = content.replace(helpers_listener_end, billing_listener)

# 4. Helfer-Export: Telefon-Spalte auch entfernen
print("4️⃣ Entferne Telefon-Spalte aus Helfer-Export...")

old_helper_data = '''            }).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Telefon': p.telefon || 'Nicht angegeben',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));
            
            const headers = ['Name', 'E-Mail', 'Telefon', 'Aufbau (22.08.)', 'Abbau (24.08.)', 'Hinweise'];'''

new_helper_data = '''            }).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));
            
            const headers = ['Name', 'E-Mail', 'Aufbau (22.08.)', 'Abbau (24.08.)', 'Hinweise'];'''

content = content.replace(old_helper_data, new_helper_data)

# 5. Buffet-Export: Telefon-Spalte auch entfernen
print("5️⃣ Entferne Telefon-Spalte aus Buffet-Export...")

old_buffet_push = '''                            buffetItems.push({
                                'Gericht': item.item || item.name || 'Unbekannt',
                                'Anbieter': p.name,
                                'Portionen': item.quantity || 'Nicht angegeben',
                                'E-Mail': p.email,
                                'Telefon': p.telefon || 'Nicht angegeben'
                            });'''

new_buffet_push = '''                            buffetItems.push({
                                'Gericht': item.item || item.name || 'Unbekannt',
                                'Anbieter': p.name,
                                'Portionen': item.quantity || 'Nicht angegeben',
                                'E-Mail': p.email
                            });'''

content = content.replace(old_buffet_push, new_buffet_push)

old_buffet_push2 = '''                            buffetItems.push({
                                'Gericht': p.buffet.replace(/"/g, ''),
                                'Anbieter': p.name,
                                'Portionen': p.quantity || 'Nicht angegeben',
                                'E-Mail': p.email,
                                'Telefon': p.telefon || 'Nicht angegeben'
                            });'''

new_buffet_push2 = '''                            buffetItems.push({
                                'Gericht': p.buffet.replace(/"/g, ''),
                                'Anbieter': p.name,
                                'Portionen': p.quantity || 'Nicht angegeben',
                                'E-Mail': p.email
                            });'''

content = content.replace(old_buffet_push2, new_buffet_push2)

# Buffet-Headers anpassen
old_buffet_headers = "const headers = ['Gericht', 'Anbieter', 'Portionen', 'E-Mail', 'Telefon'];"
new_buffet_headers = "const headers = ['Gericht', 'Anbieter', 'Portionen', 'E-Mail'];"

content = content.replace(old_buffet_headers, new_buffet_headers)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSV-Export-Optimierung abgeschlossen!")
print("   → Telefon-Spalte aus allen Exports entfernt")
print("   → Grillbuffet-/Getränke-Präferenzen aus Teilnehmerliste entfernt") 
print("   → Neuer Export 'Abrechnung' mit 5 Spalten hinzugefügt")
print("   → Teilnehmerliste: 10 Spalten (von 13)")
print("   → Helfer-Liste: 5 Spalten (von 6)")
print("   → Buffet-Planung: 4 Spalten (von 5)")
print("   → NEU Abrechnung: 5 Spalten (Name, Loge, Begleitung, Gesamtpersonen, Bezahlt)")
