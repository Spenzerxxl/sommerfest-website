#!/usr/bin/env python3
import re

print("🔧 TOTAL-REPARATUR: CSV-Export System komplett neu schreiben...")

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Alte convertToCSV Funktion komplett ersetzen
print("1️⃣ Ersetze convertToCSV() Funktion mit benutzerfreundlicher Version...")

old_convert_csv = '''function convertToCSV(data) {
            if (!data || data.length === 0) return '';
            
            const headers = Object.keys(data[0]);
            const csvHeaders = headers.join(',');
            const csvRows = data.map(row => 
                headers.map(header => `"${(row[header] || '').toString().replace(/"/g, '""')}"`).join(',')
            );
            
            return [csvHeaders, ...csvRows].join('\\n');
        }'''

new_convert_csv = '''function convertToCSV(data, headers) {
            if (!data || data.length === 0) return '';
            
            // CSV-Headers (deutsche Spalten-Namen)
            const csvHeaders = headers.map(h => `"${h}"`).join(';');
            
            // CSV-Zeilen mit sauberer Formatierung
            const csvRows = data.map(row => 
                headers.map(header => {
                    let value = (row[header] || '').toString();
                    // Anführungszeichen escapen und Text in Anführungszeichen setzen
                    value = value.replace(/"/g, '""');
                    return `"${value}"`;
                }).join(';')
            );
            
            return [csvHeaders, ...csvRows].join('\\n');
        }'''

content = content.replace(old_convert_csv, new_convert_csv)

# 2. Alle Event-Listener komplett ersetzen mit sauberer Datenaufbereitung
print("2️⃣ Ersetze alle Export-Event-Listener mit sauberer Datenaufbereitung...")

# Pattern um alle alten Event-Listener zu finden
old_listeners_pattern = r'// Export-Event-Listener[\s\S]*?// Initial Load'

# Neue, saubere Event-Listener
new_listeners = '''// Export-Event-Listener (komplett überarbeitet für Excel-Kompatibilität)
        document.getElementById('exportAll').addEventListener('click', function() {
            console.log('Export Teilnehmerliste gestartet...');
            
            const participantData = currentData.participants.map(p => {
                // Lodge-Mapping anwenden
                const lodge = mapLodgeFromData(p.email, p.name);
                
                // Gäste-Korrektur anwenden  
                const correctedData = correctGuestDataFromPattern(p);
                const guests = correctedData ? correctedData.gaeste : (p.gaeste || 'Keine');
                const totalPersons = correctedData ? correctedData.personen : (parseInt(p.personen) || 1);
                
                // Datum formatieren
                const formattedDate = p.datum ? new Date(p.datum).toLocaleDateString('de-DE') : 'Nicht angegeben';
                
                // Buffet-Beiträge aufbereiten
                let buffetItems = 'Keine Angabe';
                if (p.buffet) {
                    try {
                        const buffetData = JSON.parse(p.buffet);
                        buffetItems = buffetData.map(item => `${item.item} (${item.quantity} Portionen)`).join(', ');
                    } catch (e) {
                        buffetItems = p.buffet.replace(/"/g, '') || 'Keine Angabe';
                    }
                }
                
                return {
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
                };
            });
            
            const headers = ['Name', 'E-Mail', 'Telefon', 'Loge', 'Begleitung', 'Gesamt-Personen', 'Anmeldedatum', 'Buffet-Beiträge', 'Aufbau-Helfer', 'Abbau-Helfer', 'Hinweise', 'Grillbuffet-Präferenzen', 'Getränke-Präferenzen'];
            
            exportToCSV(participantData, headers, 'sommerfest_teilnehmer_komplett.csv');
        });

        document.getElementById('exportPreferences').addEventListener('click', function() {
            console.log('Export Präferenzen gestartet...');
            
            const prefData = currentData.participants.map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Grillbuffet-Präferenzen': p.grillbuffet_praeferenzen || 'Keine Angabe',
                'Grillbuffet-Bemerkungen': p.grillbuffet_bemerkungen || 'Keine',
                'Getränke-Präferenzen': p.getraenke_praeferenzen || 'Keine Angabe',
                'Getränke-Bemerkungen': p.getraenke_bemerkungen || 'Keine'
            }));
            
            const headers = ['Name', 'E-Mail', 'Grillbuffet-Präferenzen', 'Grillbuffet-Bemerkungen', 'Getränke-Präferenzen', 'Getränke-Bemerkungen'];
            
            exportToCSV(prefData, headers, 'sommerfest_praeferenzen.csv');
        });

        document.getElementById('exportBuffet').addEventListener('click', function() {
            console.log('Export Buffet-Planung gestartet...');
            
            const buffetItems = [];
            currentData.participants.forEach(p => {
                if (p.buffet) {
                    try {
                        const buffetData = JSON.parse(p.buffet);
                        buffetData.forEach(item => {
                            buffetItems.push({
                                'Gericht': item.item || item.name || 'Unbekannt',
                                'Anbieter': p.name,
                                'Portionen': item.quantity || 'Nicht angegeben',
                                'E-Mail': p.email,
                                'Telefon': p.telefon || 'Nicht angegeben'
                            });
                        });
                    } catch (e) {
                        if (p.buffet.trim()) {
                            buffetItems.push({
                                'Gericht': p.buffet.replace(/"/g, ''),
                                'Anbieter': p.name,
                                'Portionen': p.quantity || 'Nicht angegeben',
                                'E-Mail': p.email,
                                'Telefon': p.telefon || 'Nicht angegeben'
                            });
                        }
                    }
                }
            });
            
            const headers = ['Gericht', 'Anbieter', 'Portionen', 'E-Mail', 'Telefon'];
            
            exportToCSV(buffetItems, headers, 'sommerfest_buffet_planung.csv');
        });

        document.getElementById('exportHelpers').addEventListener('click', function() {
            console.log('Export Helfer-Liste gestartet...');
            
            const helperData = currentData.participants.filter(p => 
                (p.helfer_aufbau && p.helfer_aufbau.includes('Ja')) || 
                (p.helfer_abbau && p.helfer_abbau.includes('Ja'))
            ).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Telefon': p.telefon || 'Nicht angegeben',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));
            
            const headers = ['Name', 'E-Mail', 'Telefon', 'Aufbau (22.08.)', 'Abbau (24.08.)', 'Hinweise'];
            
            exportToCSV(helperData, headers, 'sommerfest_helfer_liste.csv');
        });

        // Initial Load'''

content = re.sub(old_listeners_pattern, new_listeners, content, flags=re.DOTALL)

# 3. exportToCSV Funktion erweitern um headers-Parameter
print("3️⃣ Aktualisiere exportToCSV() Funktionssignatur...")

old_export_function = '''function exportToCSV(data, filename) {
            const csv = convertToCSV(data);
            // UTF-8 BOM hinzufügen für korrekte deutsche Umlaute
            const csvWithBOM = '\\ufeff' + csv;
            const blob = new Blob([csvWithBOM], { type: 'text/csv;charset=utf-8;' });'''

new_export_function = '''function exportToCSV(data, headers, filename) {
            console.log(`Erstelle CSV: ${filename} mit ${data.length} Zeilen`);
            const csv = convertToCSV(data, headers);
            // UTF-8 BOM hinzufügen für korrekte deutsche Umlaute
            const csvWithBOM = '\\ufeff' + csv;
            const blob = new Blob([csvWithBOM], { type: 'text/csv;charset=utf-8;' });'''

content = content.replace(old_export_function, new_export_function)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSV-Export-System komplett neu geschrieben!")
print("   → convertToCSV() mit deutsche Headers und Semikolon-Trennung")
print("   → Alle Event-Listener mit sauberer Datenaufbereitung")
print("   → JSON-Buffet-Daten werden korrekt geparst")
print("   → Excel-kompatible Formatierung")
print("   → UTF-8 BOM für deutsche Umlaute")
