# Lese die Datei
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fehler 1: querySelectorAll-Syntax korrigieren
old_query = '''const dynamicItems = document.querySelectorAll("[id^=contribution][id!=contribution], [id^=quantity][id!=quantity]");'''
new_query = '''const dynamicItems = document.querySelectorAll("[id^='contribution']:not([id='contribution']), [id^='quantity']:not([id='quantity'])");'''

content = content.replace(old_query, new_query)

# Fehler 2: liveContributionsList Existenzprüfung hinzufügen
old_live = '''const liveList = document.getElementById("liveContributionsList");
                liveList.innerHTML = "";'''

new_live = '''const liveList = document.getElementById("liveContributionsList");
                if (liveList) {
                    liveList.innerHTML = "";
                } else {
                    console.log("liveContributionsList Element nicht gefunden");
                    return;
                }'''

content = content.replace(old_live, new_live)

# Schreibe die Datei zurück
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JavaScript-Fehler behoben!")
