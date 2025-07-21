        document.getElementById('exportBilling').addEventListener('click', function() {
            console.log('Export Abrechnung (alphabetisch) gestartet...');
            
            const allPersons = [];
            
            currentData.participants.forEach(participant => {
                // Lodge-Mapping für Hauptperson
                const lodge = mapLodgeFromData(participant.email, participant.name);
                
                // Gäste-Korrektur anwenden  
                const correctedData = correctGuestDataFromPattern(participant);
                const guests = correctedData ? correctedData.gaeste : (participant.gaeste || 'Keine');
                
                // 1. HAUPTPERSON HINZUFÜGEN
                allPersons.push({
                    'Name': participant.name || 'N/A',
                    'Loge/Gastgeber': lodge,
                    'Bezahlt': ''
                });
                
                // 2. GÄSTE HINZUFÜGEN
                if (guests && guests !== 'Keine' && guests.trim() !== '') {
                    // Gäste-Namen splitten und säubern
                    const guestNames = guests.split(',')
                        .map(name => name.trim())
                        .filter(name => name.length > 0);
                    
                    guestNames.forEach(guestName => {
                        allPersons.push({
                            'Name': guestName,
                            'Loge/Gastgeber': `Gast von ${participant.name}`,
                            'Bezahlt': ''
                        });
                    });
                }
            });
            
            // 3. ALPHABETISCH SORTIEREN
            allPersons.sort((a, b) => a.Name.localeCompare(b.Name));
            
            // 4. CSV EXPORT
            const headers = ['Name', 'Loge/Gastgeber', 'Bezahlt'];
            
            console.log('Abrechnungs-Daten (alphabetisch):', allPersons);
            exportToCSV(allPersons, headers, 'sommerfest_abrechnung_alphabetisch.csv');
        });
