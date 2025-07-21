#!/usr/bin/env python3
"""
Komplette Sidebar-Optimierung: Getränke verschieben + rechte Sidebar vereinfachen
"""

def move_getraenke_to_sidebar():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Getränke-Sektion aus Hauptformular extrahieren
    getraenke_start = content.find('<h2>Getränke-Präferenzen</h2>')
    getraenke_end = content.find('<button type="submit" class="button">Anmeldung absenden</button>')
    
    if getraenke_start == -1 or getraenke_end == -1:
        print("❌ Getränke-Sektion nicht gefunden!")
        return
    
    getraenke_section = content[getraenke_start:getraenke_end].strip()
    
    # 2. Aus Hauptformular entfernen
    content = content[:getraenke_start] + content[getraenke_end:]
    
    # 3. Zu Sidebar-Format konvertieren
    sidebar_getraenke = getraenke_section
    
    # H2 zu H3 ändern und Emoji hinzufügen
    sidebar_getraenke = sidebar_getraenke.replace('<h2>Getränke-Präferenzen</h2>', 
                                                 '<h3>🍺 Getränke-Präferenzen</h3>')
    
    # Styling zu Sidebar-Klassen ändern
    sidebar_getraenke = sidebar_getraenke.replace(
        'style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px;"',
        'class="checkbox-group"'
    )
    sidebar_getraenke = sidebar_getraenke.replace(
        'style="display: flex; align-items: center; gap: 5px;"',
        'class="checkbox-item"'
    )
    sidebar_getraenke = sidebar_getraenke.replace(
        'style="font-weight: normal; margin-bottom: 0;"',
        ''
    )
    sidebar_getraenke = sidebar_getraenke.replace(
        '<textarea id="getraenke_bemerkungen"',
        '<textarea class="preferences-textarea" id="getraenke_bemerkungen"'
    )
    
    # Form-groups zu preferences-category ändern
    sidebar_getraenke = sidebar_getraenke.replace('<div class="form-group">', '<div class="preferences-category">')
    sidebar_getraenke = sidebar_getraenke.replace('<label>', '<h5>')
    sidebar_getraenke = sidebar_getraenke.replace('</label>', '</h5>')
    
    # In preferences-section wrapper einbetten
    sidebar_getraenke_wrapped = f'''
            <div class="preferences-section">
                {sidebar_getraenke}
            </div>'''
    
    # 4. In linke Sidebar einfügen (nach grillbuffet_bemerkungen)
    insertion_point = content.find('</div>\n\n        <div class="main-content">')
    if insertion_point == -1:
        print("❌ Einfügepunkt in linker Sidebar nicht gefunden!")
        return
    
    content = content[:insertion_point] + sidebar_getraenke_wrapped + '\n        ' + content[insertion_point:]
    
    print("✅ Getränke-Präferenzen in linke Sidebar verschoben")
    
    # 5. Rechte Sidebar vereinfachen
    # Finde rechte Sidebar
    sidebar_start = content.find('<!-- Bestehende Buffet-Sidebar (Rechts) -->')
    if sidebar_start == -1:
        print("❌ Rechte Sidebar nicht gefunden!")
        return
    
    sidebar_end = content.find('</div>\n    </div>\n\n    <script>', sidebar_start)
    if sidebar_end == -1:
        print("❌ Ende der rechten Sidebar nicht gefunden!")
        return
    
    # Neue vereinfachte Sidebar
    simple_sidebar = '''<!-- Vereinfachte Buffet-Sidebar (Rechts) -->
        <div class="sidebar">
            <h3>Bisherige Buffet-Beiträge</h3>
            <ul id="contributionsList" class="contribution-list">
            </ul>
        </div>'''
    
    content = content[:sidebar_start] + simple_sidebar + content[sidebar_end:]
    
    print("✅ Rechte Sidebar vereinfacht")
    
    # 6. loadHelferStatistik entfernen (falls vorhanden)
    if 'loadHelferStatistik' in content:
        # Entferne Funktionsaufruf
        content = content.replace('loadHelferStatistik();', '')
        content = content.replace('window.addEventListener(\'load\', loadHelferStatistik);', '')
        print("✅ loadHelferStatistik-Aufrufe entfernt")
    
    # 7. Datei speichern
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Alle Sidebar-Optimierungen erfolgreich abgeschlossen!")

if __name__ == "__main__":
    move_getraenke_to_sidebar()
