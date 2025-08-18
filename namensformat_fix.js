        // Hilfsfunktion: "Frank Rath" → "Rath, Frank" für Kassenliste
        function formatNameForBilling(fullName) {
            if (!fullName || fullName === 'N/A') return fullName;
            
            const parts = fullName.trim().split(' ');
            if (parts.length < 2) return fullName; // Nur ein Name
            
            // Letzter Teil = Nachname, Rest = Vorname(n)
            const lastName = parts[parts.length - 1];
            const firstName = parts.slice(0, -1).join(' ');
            
            return `${lastName}, ${firstName}`;
        }

