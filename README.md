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

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-04-23 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

## Historique

Le script enregistre automatiquement chaque taux de change dans le fichier `exchange_rate_history.csv` pour suivre l'évolution quotidienne des taux. Le fichier contient :
- Date
- Heure
- Taux de change (JPY par EUR)

Exemple de fichier historique :
```
Date,Time,Rate (JPY per EUR)
2026-09-17,05:03:59,152.45
2026-09-17,05:04:04,152.45
```

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- Un historique complet est maintenu dans `exchange_rate_history.csv`
- En cas d'indisponibilité de l'API, le script utilise un cache ou une valeur par défaut
