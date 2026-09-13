#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and track daily rates
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'eur_jpy_history.csv'
FALLBACK_RATE = 152.45

def get_eur_jpy_rate(use_cache=True):
    """Fetch current EUR/JPY exchange rate from an API"""
    try:
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
                        rate = data['rates'].get('JPY')

                    if rate:
                        save_cache(rate)
                        log_daily_rate(rate)
                        display_rate(rate, source="API")
                        return rate
            except Exception:
                continue

        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                print(f"\n{'='*50}")
                print("⚠️  Données en cache (connexion API échouée)")
                print(f"{'='*50}")
                display_rate(cached_rate, source="Cache")
                return cached_rate

        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE, source="Par défaut")
        log_daily_rate(FALLBACK_RATE)
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_rate(rate, source=""):
    """Display the exchange rate"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Taux de change EUR/JPY - {timestamp}")
    if source:
        print(f"Source: {source}")
    print(f"{'='*50}")
    print(f"1 EUR = {rate:.2f} JPY")
    print(f"{'='*50}\n")


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


def log_daily_rate(rate):
    """Log the rate to CSV history file (one entry per day)"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        file_exists = os.path.exists(HISTORY_FILE)

        if file_exists:
            with open(HISTORY_FILE, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            if rows and rows[-1].get('date') == today:
                return

        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'rate', 'time'])

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'date': today,
                'rate': f'{rate:.2f}',
                'time': datetime.now().strftime('%H:%M:%S')
            })
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'historique: {e}")


def display_history(last_n=7):
    """Display recent exchange rate history"""
    try:
        if not os.path.exists(HISTORY_FILE):
            print("Aucun historique disponible")
            return

        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("Aucun historique disponible")
            return

        print(f"\n{'='*50}")
        print(f"Historique EUR/JPY (derniers {last_n} jours)")
        print(f"{'='*50}")
        print(f"{'Date':<12} {'Taux':<10} {'Heure':<10}")
        print(f"{'-'*50}")

        for row in rows[-last_n:]:
            print(f"{row['date']:<12} {row['rate']:<10} {row['time']:<10}")

        print(f"{'='*50}\n")
    except Exception as e:
        print(f"Erreur lors de l'affichage de l'historique: {e}")


if __name__ == "__main__":
    get_eur_jpy_rate()
    display_history()
