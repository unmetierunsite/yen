# Exécution Planifiée

Ce script est conçu pour être exécuté quotidiennement afin de tracker les taux de change EUR/JPY.

## Configuration avec Cron

Pour exécuter le script automatiquement chaque jour à une heure spécifique (ex: 8h du matin), ajoutez une ligne à votre crontab :

```bash
crontab -e
```

Puis ajoutez :
```
0 8 * * * cd /home/user/yen && python3 exchange_rate.py >> exchange_rate.log 2>&1
```

Cela exécutera le script tous les jours à 8h00 et enregistrera les logs dans `exchange_rate.log`.

## Fichiers Générés

- `daily_rates.csv` : Historique des taux de change quotidiens
- `exchange_rate_cache.json` : Cache du dernier taux connu (pour les appels API échoués)
- `exchange_rate.log` : Logs d'exécution (si configuré avec cron)

## Variables d'Environnement

Vous pouvez customiser le comportement du script via des variables d'environnement :
- `EXCHANGE_RATE_API` : URL de l'API à utiliser
- `FALLBACK_RATE` : Taux de change par défaut à utiliser

## Exemple de Sortie

```
==================================================
Taux de change EUR/JPY - 2026-09-09 08:00:15
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
Taux de change EUR/JPY - Derniers 7 jours
==================================================
2026-09-09: 1 EUR = 152.45 JPY
2026-09-08: 1 EUR = 151.80 JPY
2026-09-07: 1 EUR = 152.10 JPY
2026-09-06: 1 EUR = 151.95 JPY
2026-09-05: 1 EUR = 152.30 JPY
2026-09-04: 1 EUR = 151.70 JPY
2026-09-03: 1 EUR = 152.00 JPY
==================================================
```
