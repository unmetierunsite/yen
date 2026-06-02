# EUR/JPY Exchange Rate Tracker

Un script pour tracker le taux de change quotidien entre l'Euro et le Yen Japonais avec historique.

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

### Afficher l'historique quotidien
```bash
python exchange_rate.py --history
```

## Fonctionnalités

- **Taux en temps réel** : Récupère le taux EUR/JPY actuel via API
- **Historique** : Enregistre automatiquement chaque taux quotidien
- **Statistiques** : Affiche les statistiques (moyenne, min, max, tendance)
- **Cache** : Fallback en cache en cas d'indisponibilité de l'API
- **Redondance** : Utilise plusieurs APIs pour fiabilité

## Output du taux actuel

```
==================================================
Taux de change EUR/JPY - 2026-04-23 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

## Output de l'historique

```
============================================================
HISTORIQUE DU TAUX EUR/JPY
============================================================

2026-04-20:
  Moyenne: 150.23 JPY
  Min: 149.80 JPY | Max: 151.50 JPY
  Observations: 2

2026-04-21:
  Moyenne: 152.45 JPY
  Min: 152.10 JPY | Max: 152.80 JPY
  Observations: 1

============================================================
STATISTIQUES GLOBALES
============================================================
Jours suivis: 2
Taux moyen: 151.34 JPY
Taux minimum: 149.80 JPY
Taux maximum: 152.80 JPY

Tendance: 📈 À la hausse
Variation: +2.22 JPY (+1.48%)
============================================================
```

## Notes

- L'API utilisée est gratuite et ne nécessite pas de clé API
- Les données sont sauvegardées automatiquement dans `exchange_rate_history.json`
- Pour un suivi quotidien automatique, vous pouvez configurer une tâche cron ou un planificateur
