#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and log historical data
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
                        log_rate(rate)
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
                log_rate(cached_rate)
                display_rate(cached_rate)
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        log_rate(FALLBACK_RATE)
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

    # Display statistics if history exists
    stats = get_statistics()
    if stats:
        print("Statistiques (historique):")
        print(f"  Moyenne: {stats['average']:.2f} JPY")
        print(f"  Minimum: {stats['min']:.2f} JPY (le {stats['min_date']})")
        print(f"  Maximum: {stats['max']:.2f} JPY (le {stats['max_date']})")
        print(f"  Jours tracés: {stats['count']}\n")


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


def log_rate(rate):
    """Log the exchange rate to CSV history file"""
    try:
        date_str = datetime.now().strftime('%Y-%m-%d')
        timestamp_str = datetime.now().isoformat()

        file_exists = os.path.exists(HISTORY_FILE)

        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Timestamp', 'Rate_JPY'])
            writer.writerow([date_str, timestamp_str, f'{rate:.2f}'])
    except Exception:
        pass


def get_statistics():
    """Calculate statistics from history"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return None

        rates = []
        dates = []

        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    rate = float(row['Rate_JPY'])
                    rates.append(rate)
                    dates.append(row['Date'])
                except (ValueError, KeyError):
                    continue

        if not rates:
            return None

        return {
            'average': sum(rates) / len(rates),
            'min': min(rates),
            'max': max(rates),
            'min_date': dates[rates.index(min(rates))],
            'max_date': dates[rates.index(max(rates))],
            'count': len(rates)
        }
    except Exception:
        return None


if __name__ == "__main__":
    get_eur_jpy_rate()
