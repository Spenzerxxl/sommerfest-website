#!/usr/bin/env python3

with open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Finde die Zeile mit tab-participants und entferne die active Klasse und display:block
for i, line in enumerate(lines):
    if 'id="tab-participants"' in line:
        # Entferne active und display:block aus dieser Zeile
        lines[i] = line.replace(' active', '').replace(' style="display: block;"', '')
        print(f"Zeile {i+1} korrigiert: tab-participants ist nicht mehr standardmäßig aktiv")
        break

# Schreibe die korrigierte Version
with open('admin.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("admin.html wurde korrigiert")
