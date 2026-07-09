# EUR/JPY Exchange Rate Tracker

Un script pour suivre le taux de change quotidien entre l'Euro et le Yen Japonais avec historique.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Obtenir le taux du jour
```bash
python exchange_rate.py
```

Affiche le taux de change actuel EUR/JPY et l'enregistre automatiquement dans l'historique.

**Exemple de sortie:**
```
==================================================
Taux de change EUR/JPY - 2026-07-09 05:04:34
==================================================
1 EUR = 152.45 JPY
==================================================
```

### Voir l'historique des taux
```bash
python show_history.py
```

Affiche tout l'historique des taux enregistrés avec statistiques.

Pour afficher seulement les N derniers jours :
```bash
python show_history.py 7    # Derniers 7 jours
python show_history.py 30   # Derniers 30 jours
```

**Exemple de sortie:**
```
============================================================
Historique du Taux de Change EUR/JPY
============================================================
Date         | Taux (JPY)     
------------------------------------------------------------
2026-07-09   | 152.45         
============================================================

Statistiques:
  Premier taux: 152.45 JPY (2026-07-09)
  Dernier taux: 152.45 JPY (2026-07-09)
  Variation: +0.00 JPY (+0.00%)
  Total entrées: 1
```

## Fonctionnalités

- **Récupération automatique** du taux quotidien via API gratuite
- **Historique CSV** pour suivre les variations jour après jour
- **Système de cache** en cas de défaut connexion API
- **Valeur par défaut** de secours si les APIs ne répondent pas
- **Statistiques** incluant la variation en JPY et en pourcentage

## Fichiers

- `exchange_rate.py` - Script principal pour récupérer le taux
- `show_history.py` - Script pour afficher l'historique
- `exchange_rate_history.csv` - Fichier d'historique (créé automatiquement)
- `exchange_rate_cache.json` - Cache du dernier taux (créé automatiquement)

## Notes

- L'API utilisée (exchangerate-api.com) est gratuite et ne nécessite pas de clé API
- Fallback sur une API alternative en cas d'indisponibilité
- Les taux sont enregistrés une fois par jour (à chaque exécution du script)
- Pour un suivi automatisé quotidien, utilisez une tâche cron ou un scheduler
