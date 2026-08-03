#!/usr/bin/env python3
"""
Script to display and track EUR/JPY exchange rate daily
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
RATES_CSV = 'exchange_rates_history.csv'
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


def log_rate_to_csv(rate):
    """Log the exchange rate to a CSV file for historical tracking"""
    try:
        timestamp = datetime.now().isoformat()
        date = datetime.now().strftime('%Y-%m-%d')

        file_exists = os.path.exists(RATES_CSV)

        with open(RATES_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Timestamp', 'EUR_to_JPY_Rate'])
            writer.writerow([date, timestamp, f'{rate:.2f}'])
    except Exception:
        pass


def get_recent_rates(days=7):
    """Get the recent rates from CSV file"""
    try:
        if not os.path.exists(RATES_CSV):
            return []

        rates = []
        with open(RATES_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rates.append(row)

        return rates[-days:] if rates else []
    except Exception:
        return []


def display_summary():
    """Display recent exchange rates summary"""
    rates = get_recent_rates(7)

    if not rates:
        return

    print(f"\n{'='*50}")
    print("📊 Derniers taux de change (7 derniers jours)")
    print(f"{'='*50}")

    values = [float(r['EUR_to_JPY_Rate']) for r in rates]

    for rate in rates:
        print(f"{rate['Date']} : {rate['EUR_to_JPY_Rate']} JPY/EUR")

    if len(values) > 1:
        min_rate = min(values)
        max_rate = max(values)
        avg_rate = sum(values) / len(values)
        change = values[-1] - values[0]

        print(f"\n{'─'*50}")
        print(f"Min:     {min_rate:.2f} JPY")
        print(f"Max:     {max_rate:.2f} JPY")
        print(f"Moyenne: {avg_rate:.2f} JPY")
        print(f"Évolution: {change:+.2f} JPY")
        print(f"{'='*50}\n")
    else:
        print(f"{'='*50}\n")


if __name__ == "__main__":
    rate = get_eur_jpy_rate()
    if rate:
        log_rate_to_csv(rate)
        display_summary()
