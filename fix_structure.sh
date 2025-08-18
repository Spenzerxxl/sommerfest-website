#!/bin/bash

# 1. Erstelle die ersten 626 Zeilen (vor dem fehlplatzierten E-Mail-Tab)
sed -n '1,626p' admin.html > admin_fixed.html

# 2. Füge den E-Mail-Tab hinzu (aus der temporären Datei)
cat email_tab_content.tmp >> admin_fixed.html

# 3. Füge den Rest ab Zeile 649 hinzu (nach dem fehlplatzierten E-Mail-Tab)
sed -n '649,$p' admin.html >> admin_fixed.html

echo "Neue Struktur in admin_fixed.html erstellt"

# Zeige die Tab-Positionen zur Überprüfung
echo ""
echo "Tab-Positionen in der neuen Datei:"
grep -n "class=\"tab-content\"" admin_fixed.html
