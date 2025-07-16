# Lese die Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# SIE → DU Ersetzungen
replacements = [
    ('Sie sich anmelden', 'du dich anmeldest'),
    ('Mit Ihrer Teilnahme tragen Sie', 'Mit deiner Teilnahme trägst du'),
    ('Sie erhalten in Kürze', 'du erhältst in Kürze'),
    ('Ihre Anmeldung wurde erfolgreich', 'Deine Anmeldung wurde erfolgreich'),
    ('Ihre Anmeldung zum Sommerfest', 'Deine Anmeldung zum Sommerfest'),
    ('Was möchten Sie mitbringen', 'Was möchtest du mitbringen'),
    ('Bitte füllen Sie alle', 'Bitte fülle alle'),
    ('versuchen Sie es erneut', 'versuche es erneut'),
    ('Ihre ', 'Deine '),
    ('Ihren ', 'Deinen '),
    ('Ihrer ', 'Deiner '),
    ('Sie ', 'Du '),
]

# Ersetze alle Vorkommen
for old, new in replacements:
    content = content.replace(old, new)

# Schreibe die Datei zurück
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SIE → DU Ersetzungen abgeschlossen!")
