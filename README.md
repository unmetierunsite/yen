# EUR/JPY Exchange Rate Tracker

Un script qui affiche et suit le taux de change quotidien entre l'Euro et le Yen Japonais.

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

## Fonctionnalités

- **Taux actuel** : Affiche le taux EUR/JPY du jour
- **Historique** : Enregistre automatiquement le taux quotidien dans `exchange_rate_history.csv`
- **Cache** : Utilise un cache en cas d'échec de l'API
- **Fallback** : Taux par défaut en dernier recours

## Output

Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)
- L'historique des 7 derniers jours

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-04-23 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
Historique EUR/JPY (derniers 7 jours)
==================================================
2026-04-17: 1 EUR = 151.20 JPY
2026-04-18: 1 EUR = 151.85 JPY
2026-04-19: 1 EUR = 152.10 JPY
2026-04-20: 1 EUR = 152.45 JPY
2026-04-21: 1 EUR = 152.30 JPY
2026-04-22: 1 EUR = 152.50 JPY
2026-04-23: 1 EUR = 152.45 JPY
==================================================
```

## Fichiers générés

- `exchange_rate_cache.json` : Cache du dernier taux récupéré
- `exchange_rate_history.csv` : Historique quotidien des taux

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- Le script enregistre automatiquement un seul taux par jour (idéal pour une exécution planifiée)
