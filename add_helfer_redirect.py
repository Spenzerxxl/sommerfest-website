# Lese die Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Füge Weiterleitung zur Helferseite hinzu
old_success = '''// Nach 5 Sekunden Erfolgsmeldung ausblenden
                setTimeout(() => {
                    document.getElementById('successMessage').style.display = 'none';
                }, 5000);'''

new_success = '''// Nach 3 Sekunden zur Helferseite weiterleiten
                setTimeout(() => {
                    window.location.href = 'helfer.html';
                }, 3000);'''

content = content.replace(old_success, new_success)

# Schreibe die Datei zurück
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Weiterleitung zur Helferseite hinzugefügt!")
