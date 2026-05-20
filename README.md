# EUR/JPY Exchange Rate Tracker

Un script pour afficher le taux de change actuel entre l'Euro et le Yen Japonais, avec suivi de l'historique quotidien.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Afficher le taux actuel et sauvegarder dans l'historique
```bash
python exchange_rate.py
```

Affiche :
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

### Afficher l'historique quotidien
```bash
python exchange_rate.py history
```

Affiche le tableau complet de tous les taux de change quotidiens enregistrés :
```
============================================================
Historique des taux de change EUR/JPY
============================================================
Date         | Taux       | 1 EUR =
------------------------------------------------------------
2026-04-20   |   152.30   | 152.30 JPY
2026-04-21   |   152.45   | 152.45 JPY
2026-04-22   |   151.80   | 151.80 JPY
============================================================
```

### Afficher les statistiques
```bash
python exchange_rate.py stats
```

Affiche :
- Nombre de jours suivis
- Taux maximum et minimum
- Taux moyen
- Variation totale

Exemple :
```
============================================================
Statistiques des taux de change EUR/JPY
============================================================
Nombre de jours suivis: 3
Taux maximum: 152.45 JPY
Taux minimum: 151.80 JPY
Taux moyen: 152.18 JPY
Variation: 0.65 JPY
============================================================
```

## Fonctionnalités

- ✅ Affiche le taux actuel EUR/JPY
- ✅ Sauvegarde automatique un taux par jour (historique quotidien)
- ✅ Affichage de l'historique complet
- ✅ Statistiques sur l'évolution du taux
- ✅ Cache local en cas de problème de connexion API
- ✅ Valeur par défaut en secours

## Fichiers créés

- `exchange_rate_cache.json` : Cache du dernier taux de change
- `exchange_rate_history.json` : Historique quotidien des taux

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Un seul taux par jour est enregistré dans l'historique
- Les données en cache permettent une consultation même sans connexion internet
