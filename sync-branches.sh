#!/bin/bash
# Automatische Synchronisierung zwischen main und master Branch

echo "🔄 Synchronisiere main ↔ master Branches..."

# Aktueller Branch speichern
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Aktueller Branch: $CURRENT_BRANCH"

# Beide Branches auf neuesten Stand bringen
git fetch origin

# Auf main wechseln und pullen
git checkout main
git pull origin main

# master auf main Stand bringen
git checkout master
git reset --hard main

# main auf master Stand bringen (falls master neuer wäre)
git checkout main
git merge master --no-ff -m "Auto-sync: master → main"

# Beide Branches pushen
git push origin main --force-with-lease
git push origin master --force-with-lease

# Zurück zum ursprünglichen Branch
git checkout $CURRENT_BRANCH

echo "✅ Branches synchronisiert: main ↔ master"
