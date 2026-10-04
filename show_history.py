#!/usr/bin/env python3
"""
Display daily EUR/JPY exchange rate history
"""

import csv
import os
from datetime import datetime

LOG_FILE = 'exchange_rate_history.csv'


def show_history():
    """Display the exchange rate history"""
    if not os.path.exists(LOG_FILE):
        print("Aucun historique disponible. Exécutez d'abord exchange_rate.py")
        return

    try:
        with open(LOG_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("Historique vide")
            return

        print(f"\n{'='*60}")
        print("📊 HISTORIQUE DES TAUX EUR/JPY")
        print(f"{'='*60}")
        print(f"{'Date':<12} {'Heure':<10} {'Taux (JPY)':<15}")
        print(f"{'-'*60}")

        for row in rows:
            date = row['Date']
            timestamp = row['Timestamp'].split()[1] if ' ' in row['Timestamp'] else 'N/A'
            rate = row['Rate_JPY']
            print(f"{date:<12} {timestamp:<10} {rate:>13} JPY")

        if len(rows) > 1:
            rates = [float(row['Rate_JPY']) for row in rows]
            min_rate = min(rates)
            max_rate = max(rates)
            avg_rate = sum(rates) / len(rates)

            print(f"{'-'*60}")
            print(f"Statistiques ({len(rows)} entrées):")
            print(f"  • Minimum : {min_rate:.2f} JPY")
            print(f"  • Maximum : {max_rate:.2f} JPY")
            print(f"  • Moyenne : {avg_rate:.2f} JPY")
            print(f"  • Variation : {max_rate - min_rate:.2f} JPY")
            print(f"{'='*60}\n")

    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    show_history()
