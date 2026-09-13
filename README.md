# EUR/JPY Exchange Rate Tracker

Un script Python qui suit le taux de change quotidien entre l'Euro (EUR) et le Yen Japonais (JPY). Vous verrez combien de yen vous pouvez obtenir avec 1 euro chaque jour.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Exécutez le script pour obtenir le taux actuel :
```bash
python exchange_rate.py
```

## Fonctionnalités

### Affichage du taux actuel
- Taux de change EUR/JPY en temps réel
- Source de données (API, cache ou valeur par défaut)
- Horodatage exact

### Historique quotidien
Le script crée automatiquement un fichier `eur_jpy_history.csv` qui enregistre :
- **date** : Date du jour (YYYY-MM-DD)
- **rate** : Taux de change EUR/JPY
- **time** : Heure d'enregistrement

### Affichage de l'historique
Après chaque exécution, le script affiche les 7 derniers jours de l'historique.

Exemple de résultat :
```
==================================================
Taux de change EUR/JPY - 2026-09-13 05:04:03
Source: Par défaut
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
Historique EUR/JPY (derniers 7 jours)
==================================================
Date         Taux       Heure     
--------------------------------------------------
2026-09-13   152.45     05:04:03  
==================================================
```

## Exécution quotidienne programmée

Pour exécuter ce script automatiquement chaque jour, utilisez cron :

```bash
crontab -e
```

Ajoutez la ligne suivante pour l'exécuter tous les jours à 10:00 UTC :
```cron
0 10 * * * cd /home/user/yen && python exchange_rate.py >> exchange_rate.log 2>&1
```

## Fichiers générés

- `eur_jpy_history.csv` : Historique des taux quotidiens
- `exchange_rate_cache.json` : Cache du dernier taux récupéré
- `exchange_rate.log` : Journal des exécutions (si cron est configuré)

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Si l'API n'est pas accessible, le script utilise un taux en cache
- En dernier recours, un taux par défaut est utilisé (152.45 JPY/EUR)
- Un seul enregistrement par jour est sauvegardé dans l'historique
