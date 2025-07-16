# Lese die Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Korrigiere die Feldnamen-Mappings
old_mapping = '''                searchParams.append('name', formData.name);
                searchParams.append('email', formData.email);
                searchParams.append('lodge', formData.lodge);
                searchParams.append('companions', formData.companions);
                searchParams.append('contribution', formData.contribution);
                searchParams.append('quantity', formData.quantity);'''

new_mapping = '''                searchParams.append('name', formData.name);
                searchParams.append('email', formData.email);
                searchParams.append('loge', formData.lodge);
                searchParams.append('gaestelNamen', formData.companions);
                searchParams.append('buffet', formData.contribution);
                searchParams.append('portionen', formData.quantity);
                searchParams.append('anzahlGaeste', '');
                searchParams.append('gesamtPersonen', '');
                searchParams.append('aufbau', '');
                searchParams.append('abbau', '');
                searchParams.append('bemerkungen', '');'''

# Ersetze das Mapping
content = content.replace(old_mapping, new_mapping)

# Schreibe die Datei zurück
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Feldnamen-Mapping korrigiert!")
