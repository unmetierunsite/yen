# EUR/JPY Exchange Rate Tracker

Un système de suivi quotidien du taux de change entre l'Euro et le Yen Japonais.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Récupérer le taux actuel et l'enregistrer quotidiennement

Exécutez le script principal :
```bash
python exchange_rate.py
```

Le script :
- Récupère le taux de change EUR/JPY actuel
- L'affiche à l'écran
- L'enregistre dans `exchange_rate_history.csv` (pour suivi quotidien)

**Note**: Configurez une tâche programmée (cron, systemd timer, ou tâche planifiée) pour exécuter ce script quotidiennement.

### 2. Afficher l'historique et les statistiques

```bash
python show_history.py
```

Affiche :
- La liste complète de l'historique quotidien
- Les statistiques (minimum, maximum, moyenne, variation)

## Exemple d'Output

### exchange_rate.py
```
==================================================
Taux de change EUR/JPY - 2026-10-04 05:13:00
==================================================
1 EUR = 152.45 JPY
==================================================
```

### show_history.py
```
============================================================
📊 HISTORIQUE DES TAUX EUR/JPY
============================================================
Date         Heure      Taux (JPY)     
------------------------------------------------------------
2026-10-04   05:13:00          152.45 JPY
------------------------------------------------------------
Statistiques (1 entrées):
  • Minimum : 152.45 JPY
  • Maximum : 152.45 JPY
  • Moyenne : 152.45 JPY
  • Variation : 0.00 JPY
============================================================
```

## Fichiers

- `exchange_rate.py` : Script principal de récupération et enregistrement
- `show_history.py` : Affichage de l'historique et statistiques
- `exchange_rate_history.csv` : Historique des taux (généré automatiquement)
- `exchange_rate_cache.json` : Cache local (fallback en cas d'erreur API)

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Fallback automatique en cas d'indisponibilité de l'API
- Enregistrement quotidien permet de suivre l'évolution du taux sur la durée
