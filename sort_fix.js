            // 3. NACH NACHNAME SORTIEREN (FÜR KASSENLISTE)
            allPersons.sort((a, b) => {
                // Hilfsfunktion: Nachname aus "Vorname Nachname" extrahieren
                const getLastName = (fullName) => {
                    const parts = fullName.trim().split(' ');
                    return parts[parts.length - 1]; // Letzter Teil = Nachname
                };
                
                const lastNameA = getLastName(a.Name);
                const lastNameB = getLastName(b.Name);
                
                // Nach Nachname sortieren für Kassenliste  
                return lastNameA.localeCompare(lastNameB);
            });
