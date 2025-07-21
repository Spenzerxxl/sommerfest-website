# Lese die aktuelle Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fehlende Funktionen
missing_functions = '''
        let buffetItemCount = 1;

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
'''

# Finde die Stelle vor dem registrationForm Event Listener
insert_position = content.find("document.getElementById('registrationForm')")
if insert_position != -1:
    # Finde den Anfang der Zeile
    line_start = content.rfind('\n', 0, insert_position) + 1
    
    # Füge die Funktionen ein
    new_content = content[:line_start] + missing_functions + '\n        // Formular-Submit Handler\n        ' + content[line_start:]
    
    # Schreibe die Datei
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fehlende Funktionen erfolgreich hinzugefügt!")
else:
    print("FEHLER: Konnte registrationForm Event Listener nicht finden!")
