#!/bin/bash
# Setup script to configure daily EUR/JPY exchange rate tracking

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/exchange_rate.py"
CRON_JOB="0 10 * * * cd $SCRIPT_DIR && python3 $SCRIPT_PATH >> exchange_rate.log 2>&1"

echo "Configuration de la tâche quotidienne EUR/JPY"
echo "=============================================="
echo ""
echo "Cron job qui sera ajouté :"
echo "$CRON_JOB"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
    echo "La tâche est déjà configurée dans crontab"
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✓ Tâche quotidienne configurée avec succès!"
    echo "  Heure d'exécution : 10:00 UTC (tous les jours)"
    echo "  Journal : $SCRIPT_DIR/exchange_rate.log"
fi

echo ""
echo "Pour vérifier la tâche cron :"
echo "  crontab -l"
echo ""
echo "Pour supprimer la tâche cron :"
echo "  crontab -e"
