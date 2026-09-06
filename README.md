# EUR/JPY Exchange Rate Tracker

Un script qui affiche le taux de change actuel entre l'Euro et le Yen Japonais et enregistre l'historique quotidien.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Obtenir le taux du jour
Exécutez le script principal :
```bash
python exchange_rate.py
```

### Voir l'historique complet
Affichez l'historique des taux enregistrés :
```bash
python display_history.py
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

### Historique

Le script `display_history.py` affiche :
- Tous les taux enregistrés par date
- Le taux minimum, maximum et moyen
- Le taux actuel

## Fichiers générés

- `exchange_rate_cache.json` : Cache du dernier taux récupéré
- `exchange_rate_daily.json` : Historique quotidien des taux

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Les taux de change sont enregistrés quotidiennement lors de l'exécution du script
- En cas d'indisponibilité de l'API, le script utilise le cache ou une valeur par défaut
