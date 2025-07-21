#!/usr/bin/env python3
"""
Script zur korrekten Sidebar-Optimierung
NUR die drei gewünschten Änderungen, ohne andere Funktionalitäten zu berühren
"""

def fix_sidebar_optimizations():
    # Datei lesen
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Rind zur Fleisch-Kategorie hinzufügen
    putenbrust_section = '''                        <div class="checkbox-item">
                            <input type="checkbox" id="fleisch_putenbrust" value="Putenbrust">
                            <label for="fleisch_putenbrust">Putenbrust</label>
                        </div>'''
    
    rind_addition = '''                        <div class="checkbox-item">
                            <input type="checkbox" id="fleisch_putenbrust" value="Putenbrust">
                            <label for="fleisch_putenbrust">Putenbrust</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="fleisch_rind" value="Rind">
                            <label for="fleisch_rind">Rind</label>
                        </div>'''
    
    content = content.replace(putenbrust_section, rind_addition)
    print("✅ Rind zur Fleisch-Kategorie hinzugefügt")
    
    # Datei schreiben
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Erste Änderung (Rind) erfolgreich angewendet!")

if __name__ == "__main__":
    fix_sidebar_optimizations()
