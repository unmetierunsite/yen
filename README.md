# EUR/JPY Exchange Rate Tracker

Un script qui affiche le taux de change actuel entre l'Euro et le Yen Japonais et suit l'historique quotidien.

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

### Afficher l'historique des taux
```bash
# Afficher tout l'historique
python exchange_rate.py --history

# Afficher les 7 derniers jours
python exchange_rate.py --history 7

# Afficher les 30 derniers jours
python exchange_rate.py --history 30
```

## Output

Le script affiche :
- La date et l'heure actuelles
- Le taux de change EUR/JPY (combien de yen vous obtenez pour 1 euro)

Exemple - Taux actuel :
```
==================================================
Taux de change EUR/JPY - 2026-05-15 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

Exemple - Historique :
```
============================================================
Historique des taux EUR/JPY (7 jours)
============================================================
2026-05-15: 1 EUR = 152.45 JPY
2026-05-14: 1 EUR = 152.30 JPY
2026-05-13: 1 EUR = 151.85 JPY
...
============================================================
```

## Fonctionnalités

- ✅ Récupère le taux de change en temps réel
- ✅ Enregistre automatiquement chaque taux quotidien
- ✅ Affiche l'historique sur N jours
- ✅ Cache local en cas d'indisponibilité de l'API
- ✅ Valeur par défaut si l'API et le cache ne sont pas disponibles

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont récupérés quotidiennement
- L'historique est sauvegardé localement dans `exchange_rate_history.json`
- Un cache temporaire est maintenu dans `exchange_rate_cache.json`
