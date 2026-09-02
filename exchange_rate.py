#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and log to history
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.csv'
FALLBACK_RATE = 152.45


def get_eur_jpy_rate(use_cache=True):
    """Fetch current EUR/JPY exchange rate from an API"""
    rate = None

    try:
        apis = [
            'https://api.exchangerate-api.com/v4/latest/EUR',
            'https://open.er-api.com/v6/latest/EUR',
        ]

        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=5)
                data = response.json()

                if response.status_code == 200 and 'rates' in data:
                    rate = data['rates'].get('JPY')
                    if rate:
                        save_cache(rate)
                        log_to_history(rate, 'API')
                        display_rate(rate, 'API')
                        return rate
            except Exception:
                continue

        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                log_to_history(cached_rate, 'Cache')
                display_rate(cached_rate, 'Cache (API failed)')
                return cached_rate

        log_to_history(FALLBACK_RATE, 'Fallback')
        display_rate(FALLBACK_RATE, 'Fallback (value by default)')
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_rate(rate, source=''):
    """Display the exchange rate"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n{'='*50}")
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


def log_to_history(rate, source):
    """Log the exchange rate to history CSV file"""
    try:
        timestamp = datetime.now().isoformat()
        file_exists = os.path.exists(HISTORY_FILE)

        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Time', 'Rate', 'Source'])

            date_str = datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.now().strftime('%H:%M:%S')
            writer.writerow([date_str, time_str, f'{rate:.2f}', source])
    except Exception:
        pass


if __name__ == "__main__":
    get_eur_jpy_rate()
