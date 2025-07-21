# Lese die Datei
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Finde den POST-Request-Block und ersetze ihn
in_post_block = False
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Beginne Ersetzung bei "CORS-FIX"
    if "CORS-FIX" in line:
        # Füge GET-Request-Code ein
        new_lines.append("                // GET-REQUEST-LÖSUNG: Direkt zu n8n-Webhook\n")
        new_lines.append("                const searchParams = new URLSearchParams();\n")
        new_lines.append("                searchParams.append('name', formData.name);\n")
        new_lines.append("                searchParams.append('email', formData.email);\n")
        new_lines.append("                searchParams.append('lodge', formData.lodge);\n")
        new_lines.append("                searchParams.append('companions', formData.companions);\n")
        new_lines.append("                searchParams.append('contribution', formData.contribution);\n")
        new_lines.append("                searchParams.append('quantity', formData.quantity);\n")
        new_lines.append("                \n")
        new_lines.append("                const response = await fetch(`${N8N_WEBHOOK_URL}?${searchParams}`, {\n")
        new_lines.append("                    method: 'GET',\n")
        new_lines.append("                    mode: 'no-cors'  // Verhindert CORS-Probleme\n")
        new_lines.append("                });\n")
        new_lines.append("\n")
        new_lines.append("                // Bei no-cors können wir Status nicht prüfen - daher Success annehmen\n")
        
        # Überspringe bis "console.log('Anmeldung gesendet':"
        i += 1
        while i < len(lines) and "console.log('Anmeldung gesendet':" not in lines[i]:
            i += 1
        # Füge den Rest ohne die if (response.ok) Bedingung hinzu
        if i < len(lines):
            new_lines.append(lines[i])  # console.log Zeile
            i += 1
            
            # Kopiere alle Zeilen bis "} else {"
            while i < len(lines) and "} else {" not in lines[i]:
                new_lines.append(lines[i])
                i += 1
            
            # Überspringe "} else {" und "throw new Error"
            while i < len(lines) and "} catch (error) {" not in lines[i]:
                i += 1
            
            # Füge den catch-Block hinzu
            if i < len(lines):
                new_lines.append("                \n")
                new_lines.append(lines[i])  # } catch (error) {
                i += 1
                # Kopiere den catch-Block
                while i < len(lines) and lines[i].strip() != "}":
                    new_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    new_lines.append(lines[i])  # schließende }
        
    else:
        new_lines.append(line)
    
    i += 1

# Schreibe die Datei zurück
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("GET-Request-Code erfolgreich eingefügt!")
