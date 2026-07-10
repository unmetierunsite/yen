#!/usr/bin/env python3
"""
Script to track EUR/JPY exchange rate and maintain daily history
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rates_history.csv'
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
                    if 'rates' in data and 'JPY' in data['rates']:
                        rate = data['rates']['JPY']
                        break
            except Exception:
                continue

        if rate:
            save_cache(rate)
            log_daily_rate(rate)
            display_rate(rate, "✅ Données actuelles")
            return rate

        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                log_daily_rate(cached_rate)
                display_rate(cached_rate, "⚠️  Données en cache")
                return cached_rate

        display_rate(FALLBACK_RATE, "⚠️  Valeur par défaut")
        log_daily_rate(FALLBACK_RATE)
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_rate(rate, status=""):
    """Display the exchange rate"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n{'='*50}")
    if status:
        print(status)
    print(f"Taux de change EUR/JPY - {timestamp}")
    print(f"{'='*50}")
    print(f"1 EUR = {rate:.2f} JPY")
    print(f"{'='*50}")


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
    """Log the rate to history file, avoiding duplicates for same day"""
    date_str = datetime.now().strftime('%Y-%m-%d')

    file_exists = os.path.exists(HISTORY_FILE)

    if file_exists:
        with open(HISTORY_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == date_str:
                    return

    with open(HISTORY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Rate (JPY)'])
        writer.writerow([date_str, f'{rate:.2f}'])


def display_history(days=7):
    """Display recent exchange rates"""
    if not os.path.exists(HISTORY_FILE):
        print("Aucun historique disponible")
        return

    print(f"\n{'='*50}")
    print(f"Historique des 7 derniers jours")
    print(f"{'='*50}")

    with open(HISTORY_FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

        for row in rows[-days:]:
            if row:
                print(f"{row[0]} : {row[1]} JPY")

    print(f"{'='*50}\n")


if __name__ == "__main__":
    rate = get_eur_jpy_rate()
    display_history()
