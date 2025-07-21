#!/usr/bin/env python3
import re

print("🚨 SOFORTIGE REPARATUR: Helfer-Export-Funktion...")

# admin.html einlesen
with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Die defekte Helfer-Export-Funktion ersetzen mit einer robusten Version
old_helper_function = '''        document.getElementById('exportHelpers').addEventListener('click', function() {
            console.log('Export Helfer-Liste gestartet...');
            
            const helperData = currentData.participants.filter(p => 
                (p.helfer_aufbau && p.helfer_aufbau.includes('Ja')) || 
                (p.helfer_abbau && p.helfer_abbau.includes('Ja'))
            ).map(p => ({
                'Name': p.name || 'N/A',
                'E-Mail': p.email || 'N/A',
                'Aufbau (22.08.)': p.helfer_aufbau || 'Nicht angegeben',
                'Abbau (24.08.)': p.helfer_abbau || 'Nicht angegeben',
                'Hinweise': p.bemerkungen || 'Keine'
            }));
            
            const headers = ['Name', 'E-Mail', 'Aufbau (22.08.)', 'Abbau (24.08.)', 'Hinweise'];
            
            exportToCSV(helperData, headers, 'sommerfest_helfer_liste.csv');
        });'''

# Neue, robuste Helfer-Export-Funktion
new_helper_function = '''        document.getElementById('exportHelpers').addEventListener('click', function() {
            console.log('Export Helfer-Liste gestartet...');
            
            // DEBUG: Schaue was in den Daten steht
            console.log('Teilnehmer-Daten:', currentData.participants.length);
            if (currentData.participants.length > 0) {
                console.log('Beispiel-Teilnehmer:', currentData.participants[0]);
            }
            
            // ALLE Teilnehmer exportieren (nicht nur echte Helfer) für vollständige Übersicht
            const helperData = currentData.participants.map(p => {
                // Helfer-Status auswerten (flexibel)
                let aufbauStatus = 'Nein';
                let abbauStatus = 'Nein';
                
                if (p.helfer_aufbau) {
                    if (typeof p.helfer_aufbau === 'string' && p.helfer_aufbau.toLowerCase().includes('ja')) {
                        aufbauStatus = 'Ja';
                    } else if (p.helfer_aufbau === true) {
                        aufbauStatus = 'Ja';
                    } else {
                        aufbauStatus = p.helfer_aufbau;
                    }
                }
                
                if (p.helfer_abbau) {
                    if (typeof p.helfer_abbau === 'string' && p.helfer_abbau.toLowerCase().includes('ja')) {
                        abbauStatus = 'Ja';
                    } else if (p.helfer_abbau === true) {
                        abbauStatus = 'Ja';
                    } else {
                        abbauStatus = p.helfer_abbau;
                    }
                }
                
                return {
                    'Name': p.name || 'N/A',
                    'E-Mail': p.email || 'N/A',
                    'Aufbau (22.08.)': aufbauStatus,
                    'Abbau (24.08.)': abbauStatus,
                    'Hinweise': p.bemerkungen || 'Keine'
                };
            });
            
            console.log(`Helfer-Export: ${helperData.length} Einträge gefunden`);
            
            const headers = ['Name', 'E-Mail', 'Aufbau (22.08.)', 'Abbau (24.08.)', 'Hinweise'];
            
            exportToCSV(helperData, headers, 'sommerfest_helfer_liste.csv');
        });'''

content = content.replace(old_helper_function, new_helper_function)

# Datei speichern
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Helfer-Export-Funktion repariert!")
print("   → Robuste Helfer-Status-Auswertung")
print("   → Debug-Informationen hinzugefügt")
print("   → Exportiert ALLE Teilnehmer (nicht nur echte Helfer)")
print("   → Flexibles Ja/Nein-Parsing")
