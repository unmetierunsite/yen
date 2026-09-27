# EUR/JPY Exchange Rate Tracker

Un script qui affiche le taux de change actuel entre l'Euro et le Yen Japonais et qui enregistre l'historique quotidien.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Afficher le taux actuel
Exécutez le script :
```bash
python exchange_rate.py
```

### Afficher l'historique récent
Pour voir les 7 derniers jours d'historique :
```bash
python exchange_rate.py --history
```

## Output

Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)
- Sauvegarde les données dans `exchange_rate_log.csv`

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-09-27 05:13:03
==================================================
1 EUR = 152.45 JPY
==================================================
```

## Historique

L'historique est automatiquement enregistré dans `exchange_rate_log.csv` avec :
- Date (YYYY-MM-DD)
- Heure (HH:MM:SS)
- Taux de change (JPY par EUR)

Exemple d'historique :
```
Date,Time,Rate (JPY per EUR)
2026-09-27,05:13:03,152.45
2026-09-27,05:13:13,152.45
```

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- Les données historiques sont conservées dans le fichier CSV
- En cas d'échec de l'API, le dernier taux en cache est utilisé, ou une valeur par défaut approximative
