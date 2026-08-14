# EUR/JPY Exchange Rate Tracker

Un script simple qui affiche et suit le taux de change entre l'Euro et le Yen Japonais.

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

## Suivi Historique

Le script enregistre automatiquement chaque taux dans `exchange_rate_history.csv` pour suivre l'évolution du taux de change au fil du temps.

## Automatisation

### GitHub Actions
Un workflow GitHub Actions s'exécute automatiquement chaque jour à 8h30 UTC pour :
- Récupérer le taux de change actuel
- L'enregistrer dans l'historique
- Commiter et pousser les modifications

Vous pouvez également déclencher manuellement le workflow via l'onglet "Actions" de GitHub.

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont mis à jour quotidiennement
- En cas d'indisponibilité de l'API, le script utilise une valeur en cache ou un taux par défaut
- L'historique des taux est stocké dans `exchange_rate_history.csv`
