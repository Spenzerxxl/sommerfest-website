// Live Buffet Sidebar - JavaScript
let buffetData = {};
let updateInterval;
let isUpdating = false;

const BUFFET_API_URL = 'https://automatisierung.frankrath.de/webhook/buffet-uebersicht';

async function loadBuffetData() {
    if (isUpdating) return;
    
    try {
        isUpdating = true;
        showLoadingState();
        
        const response = await fetch(BUFFET_API_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        buffetData = data;
        
        updateBuffetDisplay();
        showSuccessState();
        
    } catch (error) {
        console.error('Fehler beim Laden der Buffet-Daten:', error);
        showErrorState(error.message);
    } finally {
        isUpdating = false;
    }
}

function updateBuffetDisplay() {
    const buffetContainer = document.getElementById('buffet-live-liste');
    if (!buffetContainer) return;

    if (!buffetData || Object.keys(buffetData).length === 0) {
        buffetContainer.innerHTML = '<div class="buffet-item-placeholder">Noch keine Anmeldungen</div>';
        return;
    }

    const sortedEntries = Object.entries(buffetData)
        .sort(([,a], [,b]) => b - a)
        .filter(([name, count]) => name && count > 0);

    const buffetHTML = sortedEntries.map(([name, count]) => {
        const countClass = count >= 20 ? 'count-high' : count >= 10 ? 'count-medium' : 'count-low';
        return `
            <div class="buffet-item-live">
                <span class="buffet-name">${name}</span>
                <span class="buffet-count ${countClass}">${count}</span>
            </div>
        `;
    }).join('');

    buffetContainer.innerHTML = buffetHTML;
    
    const totalBeitraege = sortedEntries.length;
    const totalPortionen = sortedEntries.reduce((sum, [,count]) => sum + count, 0);
    
    const statsContainer = document.getElementById('buffet-stats');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="buffet-stat">${totalBeitraege} verschiedene Beiträge</div>
            <div class="buffet-stat">${totalPortionen} Portionen insgesamt</div>
        `;
    }
}

function showLoadingState() {
    const statusIndicator = document.getElementById('buffet-status');
    if (statusIndicator) {
        statusIndicator.textContent = 'Aktualisiere...';
        statusIndicator.className = 'buffet-status loading';
    }
}

function showSuccessState() {
    const statusIndicator = document.getElementById('buffet-status');
    if (statusIndicator) {
        statusIndicator.textContent = `Aktualisiert: ${new Date().toLocaleTimeString()}`;
        statusIndicator.className = 'buffet-status success';
    }
}

function showErrorState(message) {
    const statusIndicator = document.getElementById('buffet-status');
    if (statusIndicator) {
        statusIndicator.textContent = `Fehler beim Laden`;
        statusIndicator.className = 'buffet-status error';
    }
}

function startAutoRefresh() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }

    loadBuffetData();
    updateInterval = setInterval(() => {
        loadBuffetData();
    }, 30000);
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('buffet-live-liste')) {
        startAutoRefresh();
    }
});

window.addEventListener('beforeunload', function() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});
