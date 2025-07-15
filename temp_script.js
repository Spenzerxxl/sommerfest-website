        // Formular-Submit Handler
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Button sofort deaktivieren
            const submitButton = document.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = "Wird verarbeitet...";
            submitButton.style.backgroundColor = "#6c757d";
            submitButton.style.cursor = "not-allowed";
            
            // Formulardaten sammeln
            const companionsValue = document.getElementById('companions').value || '';
            const gaesteArray = companionsValue ? companionsValue.split(',').map(s => s.trim()).filter(s => s.length > 0) : [];
            const anzahlGaeste = gaesteArray.length;
            const gesamtPersonen = 1 + anzahlGaeste;
            
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value || 'Keine E-Mail-Adresse',
                loge: document.getElementById('lodge').value,
                gaesteNamen: companionsValue,
                anzahlGaeste: anzahlGaeste,
                gesamtPersonen: gesamtPersonen,
                buffet: document.getElementById('contribution').value,
                portionen: document.getElementById('quantity').value,
                aufbau: 'Noch nicht angegeben',
                abbau: 'Noch nicht angegeben',
                bemerkungen: 'Noch nicht angegeben',
                timestamp: new Date().toISOString()
            };

            // Validierung
            if (!formData.name || !formData.buffet || !formData.portionen) {
                // Button wieder aktivieren bei Fehler
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                submitButton.style.backgroundColor = "#2c5282";
                submitButton.style.cursor = "pointer";
                
                document.getElementById("errorMessage").style.display = "block";
                document.getElementById("successMessage").style.display = "none";
                return;
            }

            try {
                // HINWEIS: Das Senden an n8n erfolgt erst von der Helferseite!
                // Hier nur lokale Verarbeitung und Weiterleitung
                
                // Neuen Beitrag zur Liste hinzufügen
                contributions.push({
                    item: formData.buffet,
                    quantity: formData.portionen
                });
                updateContributionsList();

                // Erfolgsanzeige
                document.getElementById('successMessage').style.display = 'block';
                document.getElementById('errorMessage').style.display = 'none';
                
                // Button-Text ändern
                submitButton.textContent = "Weiterleitung in 2 Sekunden...";
                
                // Weiterleitung zur Helferseite nach 2 Sekunden
                setTimeout(() => {
                    const params = new URLSearchParams(formData);
                    window.location.href = `helfer-debug.html?${params.toString()}`;
                }, 2000);
                
            } catch (error) {
                console.error('Fehler beim Verarbeiten:', error);
                
                // Button wieder aktivieren bei Fehler
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                submitButton.style.backgroundColor = "#2c5282";
                submitButton.style.cursor = "pointer";
                
                document.getElementById('errorMessage').textContent = 'Fehler beim Verarbeiten der Anmeldung. Bitte versuche es später erneut.';
                document.getElementById('errorMessage').style.display = 'block';
                document.getElementById('successMessage').style.display = 'none';
            }
        });
