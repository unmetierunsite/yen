#!/usr/bin/env python3
"""
Script to display and track current EUR/JPY exchange rate
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.csv'
FALLBACK_RATE = 152.45  # Default fallback rate


def get_eur_jpy_rate(use_cache=True):
    """Fetch current EUR/JPY exchange rate from an API"""
    try:
        # Try multiple APIs for redundancy
        apis = [
            'https://api.exchangerate-api.com/v4/latest/EUR',
            'https://open.er-api.com/v6/latest/EUR',
        ]

        rate = None
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=5)
                data = response.json()

                if response.status_code == 200:
                    if 'rates' in data:
                        rate = data['rates']['JPY']
                    elif 'rates' in data and 'JPY' in data['rates']:
                        rate = data['rates']['JPY']

                    if rate:
                        save_cache(rate)
                        save_to_history(rate)
                        display_rate(rate)
                        return rate
            except Exception:
                continue

        # If API fails, try cache
        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                print(f"\n{'='*50}")
                print("⚠️  Données en cache (connexion API échouée)")
                print(f"{'='*50}")
                display_rate(cached_rate)
                save_to_history(cached_rate)
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE)
        save_to_history(FALLBACK_RATE)
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_rate(rate):
    """Display the exchange rate"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Taux de change EUR/JPY - {timestamp}")
    print(f"{'='*50}")
    print(f"1 EUR = {rate:.2f} JPY")
    print(f"{'='*50}\n")


def save_to_history(rate):
    """Save rate to history CSV file"""
    try:
        file_exists = os.path.exists(HISTORY_FILE)
        timestamp = datetime.now().strftime('%Y-%m-%d')

        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Rate'])
            writer.writerow([timestamp, f'{rate:.2f}'])
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'historique: {e}")


def display_history(days=30):
    """Display historical rates"""
    if not os.path.exists(HISTORY_FILE):
        print("Aucun historique trouvé.")
        return

    try:
        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("Aucune donnée dans l'historique.")
            return

        recent_rows = rows[-days:]

        print(f"\n{'='*50}")
        print(f"Historique EUR/JPY ({len(recent_rows)} derniers jours)")
        print(f"{'='*50}")

        rates = [float(row['Rate']) for row in recent_rows]
        min_rate = min(rates)
        max_rate = max(rates)
        avg_rate = sum(rates) / len(rates)

        print(f"Minimum: {min_rate:.2f} JPY")
        print(f"Maximum: {max_rate:.2f} JPY")
        print(f"Moyenne: {avg_rate:.2f} JPY")
        print(f"{'='*50}")

        print("\nDerniers 10 jours:")
        print(f"{'Date':<12} | {'Rate':<10}")
        print("-" * 25)
        for row in recent_rows[-10:]:
            print(f"{row['Date']:<12} | {row['Rate']:<10}")
        print()
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique: {e}")


def save_cache(rate):
    """Save rate to cache file"""
    try:
        cache_data = {
            'rate': rate,
            'timestamp': datetime.now().isoformat()
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except Exception:
        pass


def load_cache():
    """Load rate from cache file"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('rate')
    except Exception:
        pass
    return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == '--history':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            display_history(days)
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python exchange_rate.py              - Affiche le taux actuel")
            print("  python exchange_rate.py --history    - Affiche l'historique (30 derniers jours)")
            print("  python exchange_rate.py --history N  - Affiche les N derniers jours")
            print("  python exchange_rate.py --help       - Affiche cette aide")
        else:
            print(f"Option inconnue: {sys.argv[1]}")
            print("Utilisez --help pour voir les options disponibles")
    else:
        get_eur_jpy_rate()
