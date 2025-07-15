// Live Buffet-Daten API
class BuffetAPI {
    constructor() {
        this.endpoint = 'https://automatisierung.frankrath.de/webhook/buffet-liste';
        this.fallbackData = [
            { beitrag: "Kartoffelsalat", portionen: "für 15 Personen", anzahl: 1 },
            { beitrag: "Frikadellen", portionen: "40 Stück", anzahl: 1 },
            { beitrag: "Gemischter Salat", portionen: "2 große Schüsseln", anzahl: 1 }
        ];
        this.updateInterval = 30000; // 30 Sekunden
        this.lastUpdate = null;
    }

    async fetchBuffetData() {
        try {
            console.log('📡 Lade echte Buffet-Daten...');
            const response = await fetch(this.endpoint, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Echte Buffet-Daten geladen:', data);
                this.lastUpdate = new Date();
                return data.buffetBeitraege || this.fallbackData;
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.warn('⚠️ Fallback zu Beispieldaten:', error.message);
            return this.fallbackData;
        }
    }

    updateBuffetList(containerId) {
        this.fetchBuffetData().then(buffetData => {
            const container = document.getElementById(containerId);
            if (!container) return;

            // Container leeren
            container.innerHTML = '';

            // Buffet-Beiträge anzeigen
            buffetData.forEach(item => {
                const li = document.createElement('li') || document.createElement('div');
                li.className = 'contribution-item';
                
                // Anzahl-Badge wenn mehrfach vorhanden
                const anzahlBadge = item.anzahl && item.anzahl > 1 
                    ? ` <span style="background:#28a745;color:white;padding:2px 6px;border-radius:10px;font-size:0.8em;">${item.anzahl}x</span>` 
                    : '';
                
                li.innerHTML = `
                    <strong>${item.beitrag}</strong>${anzahlBadge}<br>
                    Menge: ${item.portionen}
                `;
                container.appendChild(li);
            });

            // Update-Info hinzufügen
            if (this.lastUpdate) {
                const updateInfo = document.createElement('div');
                updateInfo.style.cssText = 'font-size:0.8em;color:#a0c4ff;margin-top:10px;text-align:center;';
                updateInfo.textContent = `🔄 ${this.lastUpdate.toLocaleTimeString()}`;
                container.appendChild(updateInfo);
            }
        });
    }

    startAutoUpdate(containerId) {
        // Sofort laden
        this.updateBuffetList(containerId);
        
        // Alle 30 Sekunden aktualisieren
        setInterval(() => {
            this.updateBuffetList(containerId);
        }, this.updateInterval);
        
        console.log(`🔄 Auto-Update gestartet (
