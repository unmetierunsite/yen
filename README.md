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
- Les 7 derniers jours de taux de change (historique quotidien)

Exemple :
```
==================================================
Taux de change EUR/JPY - 2026-09-09 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
Taux de change EUR/JPY - Derniers 7 jours
==================================================
2026-09-09: 1 EUR = 152.45 JPY
2026-09-08: 1 EUR = 151.80 JPY
2026-09-07: 1 EUR = 152.10 JPY
==================================================
```

## Historique Quotidien

Le script enregistre automatiquement le taux de change de chaque jour dans un fichier `daily_rates.csv`. Cela vous permet de :
- Suivre l'évolution du taux EUR/JPY au fil du temps
- Voir les 7 derniers jours à chaque exécution
- Analyser les tendances à long terme

Pour consulter l'historique complet, ouvrez le fichier `daily_rates.csv` avec un éditeur de texte ou un tableur.

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- Les données en cache et l'historique quotidien sont stockés localement
- En cas d'indisponibilité des APIs, le script utilise la dernière valeur en cache ou un taux de change par défaut
