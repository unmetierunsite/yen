# EUR/JPY Exchange Rate Tracker

Un script pour afficher et tracker le taux de change actuel entre l'Euro et le Yen Japonais quotidiennement.

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

Affiche le taux EUR/JPY du jour et enregistre le taux dans l'historique.

### Afficher l'historique
```bash
python exchange_rate.py --history          # Affiche les 30 derniers jours
python exchange_rate.py --history 7        # Affiche les 7 derniers jours
python exchange_rate.py --history 90       # Affiche les 90 derniers jours
```

## Output Exemples

### Taux actuel
```
==================================================
Taux de change EUR/JPY - 2026-06-23 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

### Historique
```
==================================================
Historique EUR/JPY (30 derniers jours)
==================================================
Minimum: 150.25 JPY
Maximum: 154.80 JPY
Moyenne: 152.45 JPY
==================================================

Derniers 10 jours:
Date         | Rate      
-------------------------
2026-06-23   | 152.45
2026-06-22   | 152.30
...
```

## Fichiers générés

- `exchange_rate_cache.json` - Cache du dernier taux (utilisé si l'API échoue)
- `exchange_rate_history.csv` - Historique quotidien des taux

## Configuration quotidienne

Pour tracker automatiquement le taux chaque jour, vous pouvez ajouter à votre crontab :

```bash
0 10 * * * cd /path/to/yen && python exchange_rate.py
```

Cela exécutera le script chaque jour à 10h00.

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux sont enregistrés quotidiennement dans `exchange_rate_history.csv`
- Si l'API est indisponible, le script utilise le dernier taux en cache
- En dernier recours, il utilise un taux par défaut approximatif
