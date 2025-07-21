// Gäste-Zahlen-Berechnung für index.html

// Funktion zur Berechnung der Gäste-Zahlen hinzufügen
function calculateGuestNumbers(companions) {
    // Leere oder undefined companions behandeln
    if (!companions || companions.trim() === '') {
        return {
            anzahlGaeste: 0,
            gesamtPersonen: 1
        };
    }
    
    // Companions aufteilen und leere Einträge entfernen
    const guestList = companions.split(',')
        .map(name => name.trim())
        .filter(name => name.length > 0);
    
    const anzahlGaeste = guestList.length;
    const gesamtPersonen = 1 + anzahlGaeste; // 1 Hauptperson + Gäste
    
    return {
        anzahlGaeste: anzahlGaeste,
        gesamtPersonen: gesamtPersonen
    };
}

// Test der Funktion
const testCompanions = "Heidi Rath, Kay Fuhrmann";
const result = calculateGuestNumbers(testCompanions);
console.log("Test:", testCompanions);
console.log("Anzahl Gäste:", result.anzahlGaeste);
console.log("Gesamt Personen:", result.gesamtPersonen);

// Leerer Test
const emptyResult = calculateGuestNumbers("");
console.log("Leer Test - Anzahl Gäste:", emptyResult.anzahlGaeste);
console.log("Leer Test - Gesamt Personen:", emptyResult.gesamtPersonen);
