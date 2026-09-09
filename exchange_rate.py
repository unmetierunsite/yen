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
DAILY_LOG_FILE = 'daily_rates.csv'
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
                        log_daily_rate(rate)
                        display_rate(rate)
                        display_daily_rates()
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
                log_daily_rate(cached_rate)
                display_daily_rates()
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE)
        log_daily_rate(FALLBACK_RATE)
        display_daily_rates()
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
    """Log the daily rate to CSV file"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        file_exists = os.path.exists(DAILY_LOG_FILE)

        with open(DAILY_LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'EUR to JPY Rate'])
            writer.writerow([today, f"{rate:.2f}"])
    except Exception:
        pass


def display_daily_rates(limit=7):
    """Display last N days of exchange rates"""
    try:
        if not os.path.exists(DAILY_LOG_FILE):
            return

        with open(DAILY_LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) <= 1:
            return

        print(f"\n{'='*50}")
        print(f"Taux de change EUR/JPY - Derniers {min(limit, len(rows)-1)} jours")
        print(f"{'='*50}")

        # Skip header and show last limit rows
        data_rows = rows[1:]
        for row in data_rows[-limit:]:
            if row and row[0] != 'Date':
                print(f"{row[0]}: 1 EUR = {row[1]} JPY")

        print(f"{'='*50}\n")
    except Exception:
        pass


if __name__ == "__main__":
    get_eur_jpy_rate()
