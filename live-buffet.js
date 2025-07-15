// Live Buffet-Sidebar
class LiveBuffet {
    constructor() {
        this.endpoint = 'https://automatisierung.frankrath.de/webhook/buffet-liste';
        this.fallback = [
            {beitrag: "Kartoffelsalat", portionen: "für 15 Personen"},
            {beitrag: "Frikadellen", portionen: "40 Stück"},
            {beitrag: "Gemischter Salat", portionen: "2 große Schüsseln"}
        ];
    }

    async loadData() {
        try {
            const response = await fetch(this.endpoint);
            if (response.ok) {
                const data = await response.json();
                return data.buffetBeitraege || this.fallback;
            }
        } catch (error) {
            console.log('Fallback zu Beispieldaten');
        }
        return this.fallback;
    }

    async updateSidebar(containerId) {
        const data = await this.loadData();
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = data.map(item => `
            <li class="contribution-item">
                <strong>${item.beitrag}</strong><br>
                Menge: ${item.portionen}
            </li>
        `).join('');
    }

    startAutoUpdate(containerId) {
        this.updateSidebar(containerId);
        setInterval(() => this.updateSidebar(containerId), 30000);
    }
}

// Auto-Start
document.addEventListener('DOMContentLoaded', () => {
    const buffet = new LiveBuffet();
    buffet.startAutoUpdate('contributionsList');
});
