# EUR/JPY Exchange Rate Tracker

Un script qui suit le taux de change EUR/JPY quotidiennement et maintient un historique.

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

## Fonctionnalités

- **Taux actuel** : Affiche le taux de change EUR/JPY en temps réel
- **Historique quotidien** : Enregistre chaque taux dans `exchange_rates_history.csv`
- **Redondance API** : Essaie plusieurs API pour fiabilité
- **Mise en cache** : Utilise une valeur en cache si l'API échoue
- **Affichage historique** : Montre les 7 derniers jours de taux

## Output

Le script affiche :
- Le taux actuel (combien de yen pour 1 euro)
- L'historique des 7 derniers jours

Exemple :
```
==================================================
✅ Données actuelles
Taux de change EUR/JPY - 2026-07-10 05:04:08
==================================================
1 EUR = 152.45 JPY
==================================================

==================================================
Historique des 7 derniers jours
==================================================
2026-07-10 : 152.45 JPY
==================================================
```

## Fichiers générés

- `exchange_rate_cache.json` : Cache du dernier taux (recréé à chaque exécution)
- `exchange_rates_history.csv` : Historique complet des taux

## Notes

- Les APIs utilisées sont gratuites et ne nécessitent pas de clé
- L'historique est mis à jour une fois par jour (vérification par date)
- Les fichiers de données sont ignorés par Git
