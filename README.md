# EUR/JPY Exchange Rate Tracker

Un script simple qui affiche et suivi le taux de change quotidien entre l'Euro et le Yen Japonais.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Afficher le taux actuel
```bash
python exchange_rate.py
```

### Afficher l'historique des 7 derniers jours
```bash
python exchange_rate.py --history 7
```

### Afficher l'historique personnalisé
```bash
python exchange_rate.py --history 30
```

## Output

Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-09-21 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

## Fonctionnalités

- ✅ Récupération du taux en temps réel via API
- ✅ Sauvegarde du cache en cas d'échec d'API
- ✅ Historique quotidien automatique dans `exchange_rate_history.json`
- ✅ Consultation de l'historique des N derniers jours
- ✅ Taux de change approximatif par défaut

## Fichiers générés

- `exchange_rate_cache.json` : Cache du dernier taux reçu
- `exchange_rate_history.json` : Historique quotidien des taux

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- L'historique se met à jour automatiquement à chaque exécution
