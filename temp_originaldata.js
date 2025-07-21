        const originalData = {
            name: urlParams.get('name') || '',
            email: urlParams.get('email') || '',
            loge: urlParams.get('loge') || '',
            gaesteNamen: urlParams.get('gaesteNamen') || '',
            anzahlGaeste: urlParams.get('anzahlGaeste') || '0',
            gesamtPersonen: urlParams.get('gesamtPersonen') || '1',
            buffet: urlParams.get('buffet') || '',
            portionen: urlParams.get('portionen') || '',
            timestamp: urlParams.get('timestamp') || '',
            // Präferenzen-Daten (ergänzt für n8n-Übertragung)
            grillbuffet_praeferenzen: urlParams.get('grillbuffet_praeferenzen') || '',
            grillbuffet_bemerkungen: urlParams.get('grillbuffet_bemerkungen') || '',
            getraenke_praeferenzen: urlParams.get('getraenke_praeferenzen') || '',
            getraenke_bemerkungen: urlParams.get('getraenke_bemerkungen') || ''
        };
