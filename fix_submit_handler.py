# Lese die aktuelle Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Vervollständige den Submit-Handler
complete_success_code = '''                console.log('Anmeldung gesendet:', formData);
                
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
        });'''

# Finde die Stelle nach "Bei no-cors können wir Status nicht prüfen - daher Success annehmen"
insert_position = content.find("// Bei no-cors können wir Status nicht prüfen - daher Success annehmen")
if insert_position != -1:
    # Finde das Ende dieser Zeile
    line_end = content.find('\n', insert_position)
    
    # Ersetze den Rest des Submit-Handlers
    new_content = content[:line_end + 1] + complete_success_code + '\n'
    
    # Finde das Ende des Submit-Handlers und füge den Rest hinzu
    remaining_start = content.find('        async function loadLiveBuffetData()')
    if remaining_start != -1:
        new_content += content[remaining_start:]
    
    # Schreibe die Datei
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Submit-Handler erfolgreich vervollständigt!")
else:
    print("FEHLER: Konnte Submit-Handler nicht finden!")
