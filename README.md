# EUR/JPY Exchange Rate Tracker

Un script simple qui affiche le taux de change actuel entre l'Euro et le Yen Japonais et suivit l'historique quotidien.

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

### Afficher l'historique des taux
```bash
python exchange_rate.py --history          # Affiche les 7 derniers jours
python exchange_rate.py --history 30       # Affiche les 30 derniers jours
```

## Output

### Taux actuel
Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-09-07 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

### Historique
Affiche le taux moyen, minimum et maximum pour chaque jour :
```
==================================================
Historique des taux (derniers 7 jours)
==================================================
2026-09-07: 152.45 JPY (min: 152.30, max: 152.60)
2026-09-06: 151.80 JPY (min: 151.75, max: 152.00)
==================================================
```

## Fonctionnalités

- ✅ Récupère le taux EUR/JPY actuel depuis une API
- ✅ Enregistre automatiquement les taux quotidiens dans un historique
- ✅ Affiche les statistiques quotidiennes (moyenne, min, max)
- ✅ Cache des données en cas d'échec de l'API
- ✅ Taux de secours en cas d'indisponibilité

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mise à jour quotidiennement
- L'historique est sauvegardé dans `exchange_rate_history.csv`
- Les fichiers cache (`exchange_rate_cache.json`) et historique (`exchange_rate_history.csv`) sont ignorés par git
