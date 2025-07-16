# Lese die aktuelle Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Neuer kompletter JavaScript-Block
new_javascript = '''    <script>
        // Simulierte Datenbank für Beiträge
        let contributions = [];
        let buffetItemCount = 1;

        // Funktion zum Hinzufügen von Buffet-Items
        function addBuffetItem() {
            buffetItemCount++;
            const container = document.getElementById("quantity").parentNode;
            const newItem = document.createElement("div");
            newItem.className = "form-group";
            newItem.innerHTML = `
                <label for="contribution${buffetItemCount}">Weiterer Beitrag ${buffetItemCount} *</label>
                <input type="text" id="contribution${buffetItemCount}" name="contribution${buffetItemCount}" required placeholder="z.B. Kartoffelsalat">
                <label for="quantity${buffetItemCount}">Menge/Anzahl *</label>
                <input type="text" id="quantity${buffetItemCount}" name="quantity${buffetItemCount}" required placeholder="z.B. für 10 Personen">
                <button type="button" onclick="removeBuffetItem(this)" class="button-secondary">Entfernen</button>
            `;
            container.parentNode.insertBefore(newItem, container.nextSibling);
        }
        
        function removeBuffetItem(button) {
            button.parentNode.remove();
        }

        // Funktion zum Sammeln aller Buffet-Beiträge
        function collectAllBuffetItems() {
            const buffetItems = [];
            
            // Hauptbeitrag
            const mainItem = document.getElementById("contribution").value;
            const mainQuantity = document.getElementById("quantity").value;
            if (mainItem && mainQuantity) {
                buffetItems.push({ item: mainItem, quantity: mainQuantity });
            }
            
            // Zusätzliche Beiträge
            for (let i = 2; i <= buffetItemCount; i++) {
                const itemElement = document.getElementById(`contribution${i}`);
                const quantityElement = document.getElementById(`quantity${i}`);
                if (itemElement && quantityElement && itemElement.value && quantityElement.value) {
                    buffetItems.push({ item: itemElement.value, quantity: quantityElement.value });
                }
            }
            
            return JSON.stringify(buffetItems);
        }

        function updateContributionsList() {
            const contributionsList = document.getElementById("contributionsList");
            contributionsList.innerHTML = "";
            
            contributions.forEach(contribution => {
                const item = document.createElement("li");
                item.textContent = `${contribution.item} (${contribution.quantity})`;
                contributionsList.appendChild(item);
            });
        }

        // n8n Webhook URL
        const N8N_WEBHOOK_URL = 'https://automatisierung.frankrath.de/webhook/sommerfest-anmeldung';

        // Formular-Submit Handler
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Formulardaten sammeln
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                lodge: document.getElementById('lodge').value,
                companions: document.getElementById('companions').value,
                contribution: collectAllBuffetItems(),
                quantity: "Siehe Buffet-Details"
            };

            // Validierung
            const buffetData = JSON.parse(formData.contribution);
            if (!formData.name || !formData.email || buffetData.length === 0) {
                document.getElementById("errorMessage").textContent = "Bitte füllen Sie alle Pflichtfelder aus.";
                document.getElementById("errorMessage").style.display = "block";
                document.getElementById("successMessage").style.display = "none";
                return;
            }

            try {
                // GET-REQUEST-LÖSUNG: Direkt zu n8n-Webhook
                const searchParams = new URLSearchParams();
                searchParams.append('name', formData.name);
                searchParams.append('email', formData.email);
                searchParams.append('lodge', formData.lodge);
                searchParams.append('companions', formData.companions);
                searchParams.append('contribution', formData.contribution);
                searchParams.append('quantity', formData.quantity);
                
                const response = await fetch(`${N8N_WEBHOOK_URL}?${searchParams}`, {
                    method: 'GET',
                    mode: 'no-cors'
                });

                // Bei no-cors können wir Status nicht prüfen - daher Success annehmen
                console.log('Anmeldung gesendet:', formData);
                
                // Neue Beiträge zur lokalen Liste hinzufügen
                const buffetItems = JSON.parse(formData.contribution);
                buffetItems.forEach(item => {
                    contributions.push({
                        item: item.item,
                        quantity: item.quantity
                    });
                });
                updateContributionsList();

                // Erfolgsanzeige
                document.getElementById('successMessage').style.display = 'block';
                document.getElementById('errorMessage').style.display = 'none';

                // Formular zurücksetzen
                this.reset();
                
                // Dynamische Buffet-Felder zurücksetzen
                const dynamicItems = document.querySelectorAll("[id^=contribution][id!=contribution], [id^=quantity][id!=quantity]");
                dynamicItems.forEach(item => item.parentNode.remove());
                buffetItemCount = 1;
                
                // Nach 5 Sekunden Erfolgsmeldung ausblenden
                setTimeout(() => {
                    document.getElementById('successMessage').style.display = 'none';
                }, 5000);
                
            } catch (error) {
                console.error('Fehler beim Senden:', error);
                document.getElementById("errorMessage").textContent = "Fehler beim Senden der Anmeldung. Bitte versuchen Sie es erneut.";
                document.getElementById("errorMessage").style.display = "block";
                document.getElementById("successMessage").style.display = "none";
            }
        });

        async function loadLiveBuffetData() {
            try {
                const response = await fetch("https://automatisierung.frankrath.de/webhook/buffet-uebersicht");
                const data = await response.json();
                
                const liveList = document.getElementById("liveContributionsList");
                liveList.innerHTML = "";
                
                data.forEach(item => {
                    const listItem = document.createElement("li");
                    listItem.textContent = `${item.contribution} (${item.quantity}) - ${item.name}`;
                    liveList.appendChild(listItem);
                });
            } catch (error) {
                console.error('Fehler beim Laden der Live-Daten:', error);
            }
        }

        // Live-Daten alle 30 Sekunden laden
        setInterval(loadLiveBuffetData, 30000);
        loadLiveBuffetData(); // Erste Ladung

    </script>
</body>
</html>'''

# Finde den aktuellen Script-Block und ersetze ihn
script_start = content.find('<script>')
if script_start != -1:
    script_end = content.find('</html>', script_start)
    if script_end != -1:
        new_content = content[:script_start] + new_javascript
        
        # Schreibe die neue Datei
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("JavaScript komplett ersetzt!")
    else:
        print("FEHLER: Konnte </html> nicht finden")
else:
    print("FEHLER: Konnte <script> nicht finden")
