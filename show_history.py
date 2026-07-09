#!/usr/bin/env python3
"""
Script to display EUR/JPY exchange rate history
"""

import csv
import os
from datetime import datetime, timedelta

HISTORY_FILE = 'exchange_rate_history.csv'


def load_history():
    """Load historical rates from CSV file"""
    if not os.path.exists(HISTORY_FILE):
        print(f"Aucun historique trouvé. Exécutez d'abord: python exchange_rate.py")
        return []

    rates = []
    try:
        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rates.append(row)
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique: {e}")
    return rates


def display_history(limit=None):
    """Display exchange rate history"""
    rates = load_history()

    if not rates:
        return

    if limit:
        rates = rates[-limit:]

    print("\n" + "="*60)
    print("Historique du Taux de Change EUR/JPY")
    print("="*60)
    print(f"{'Date':<12} | {'Taux (JPY)':<15}")
    print("-"*60)

    for rate in rates:
        print(f"{rate['Date']:<12} | {rate['Rate (JPY per EUR)']:<15}")

    print("="*60)

    if rates:
        latest = float(rates[-1]['Rate (JPY per EUR)'])
        oldest = float(rates[0]['Rate (JPY per EUR)'])
        change = latest - oldest
        change_pct = (change / oldest) * 100

        print(f"\nStatistiques:")
        print(f"  Premier taux: {oldest:.2f} JPY ({rates[0]['Date']})")
        print(f"  Dernier taux: {latest:.2f} JPY ({rates[-1]['Date']})")
        print(f"  Variation: {change:+.2f} JPY ({change_pct:+.2f}%)")
        print(f"  Total entrées: {len(rates)}")
        print()


if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    display_history(limit)
