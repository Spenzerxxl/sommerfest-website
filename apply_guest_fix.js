const fs = require('fs');

// index.html einlesen
let indexContent = fs.readFileSync('index.html', 'utf8');

// Gäste-Berechnungsfunktion hinzufügen (nach dem anderen JavaScript)
const guestCalculationFunction = `
        // Gäste-Zahlen-Berechnung
        function calculateGuestNumbers(companions) {
            if (!companions || companions.trim() === '') {
                return {
                    anzahlGaeste: 0,
                    gesamtPersonen: 1
                };
            }
            
            const guestList = companions.split(',')
                .map(name => name.trim())
                .filter(name => name.length > 0);
            
            const anzahlGaeste = guestList.length;
            const gesamtPersonen = 1 + anzahlGaeste;
            
            return {
                anzahlGaeste: anzahlGaeste,
                gesamtPersonen: gesamtPersonen
            };
        }

        // Formular-Submit Handler`;

// Funktion vor dem "Formular-Submit Handler" hinzufügen
indexContent = indexContent.replace(
    '        // Formular-Submit Handler',
    guestCalculationFunction
);

// Erste Stelle: Direkte n8n-Übertragung (Zeile 395-396)
indexContent = indexContent.replace(
    `                searchParams.append('anzahlGaeste', '');
                searchParams.append('gesamtPersonen', '');`,
    `                // Gäste-Zahlen berechnen
                const guestNumbers = calculateGuestNumbers(formData.companions);
                searchParams.append('anzahlGaeste', guestNumbers.anzahlGaeste.toString());
                searchParams.append('gesamtPersonen', guestNumbers.gesamtPersonen.toString());`
);

// Zweite Stelle: Weiterleitung zu helfer.html (Zeile 440-441)
indexContent = indexContent.replace(
    `                        anzahlGaeste: "",
                        gesamtPersonen: "",`,
    `                        anzahlGaeste: guestNumbers.anzahlGaeste.toString(),
                        gesamtPersonen: guestNumbers.gesamtPersonen.toString(),`
);

// Speichern
fs.writeFileSync('index.html', indexContent);

console.log("✅ Gäste-Zahlen-Berechnung zu index.html hinzugefügt!");
console.log("✅ Beide n8n-Aufrufe verwenden jetzt berechnete Gäste-Zahlen!");
