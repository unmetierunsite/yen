#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and log daily rates
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
LOG_FILE = 'exchange_rate_log.csv'
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
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE)
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
    log_rate(rate)


def log_rate(rate):
    """Log the exchange rate to CSV file"""
    try:
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')

        file_exists = os.path.exists(LOG_FILE)

        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Time', 'Rate (JPY per EUR)'])
            writer.writerow([date_str, time_str, f'{rate:.2f}'])
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du journal: {e}")


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


def show_recent_history(days=7):
    """Display recent exchange rates"""
    try:
        if not os.path.exists(LOG_FILE):
            print("Aucun historique disponible")
            return

        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) <= 1:
            print("Aucun historique disponible")
            return

        print(f"\n{'='*50}")
        print(f"Historique des 7 derniers jours (jusqu'à {days} entrées)")
        print(f"{'='*50}")
        print(f"{'Date':<12} {'Time':<10} {'Rate (JPY)':<12}")
        print(f"{'-'*50}")

        for row in rows[-days:]:
            if row and row[0] != 'Date':
                print(f"{row[0]:<12} {row[1]:<10} {row[2]:<12}")
        print(f"{'='*50}\n")
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--history':
        show_recent_history()
    else:
        get_eur_jpy_rate()
