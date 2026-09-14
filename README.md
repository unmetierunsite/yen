# EUR/JPY Exchange Rate Tracker

Un script simple qui affiche le taux de change actuel entre l'Euro et le Yen Japonais.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Exécutez le script :
```bash
python exchange_rate.py
```

## Output

Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)
- Les statistiques des 7 derniers jours (min, max, moyenne)

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-04-23 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
📊 Statistiques des 7 derniers jours
==================================================
Min: 150.25 JPY
Max: 155.30 JPY
Moyenne: 152.45 JPY
Enregistrements: 7
==================================================
```

## Fichiers générés

- `exchange_rate_cache.json` : Cache du dernier taux obtenu
- `exchange_rate_daily.csv` : Historique quotidien des taux de change

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
