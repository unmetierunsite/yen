#!/usr/bin/env python3
"""
Script to display and track daily EUR/JPY exchange rate
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.csv'
FALLBACK_RATE = 152.45  # Default fallback rate


def get_eur_jpy_rate(use_cache=True, log_history=True):
    """Fetch current EUR/JPY exchange rate from an API and log to history"""
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
                        if log_history:
                            log_daily_rate(rate)
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
                if log_history:
                    log_daily_rate(cached_rate)
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE)
        if log_history:
            log_daily_rate(FALLBACK_RATE)
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


def log_daily_rate(rate):
    """Log the daily exchange rate to CSV file"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if file exists and if today's rate is already logged
        file_exists = os.path.exists(HISTORY_FILE)
        already_logged = False

        if file_exists:
            with open(HISTORY_FILE, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['date'] == today:
                        already_logged = True
                        break

        # Only log if not already logged today
        if not already_logged:
            with open(HISTORY_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'rate', 'timestamp'])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({'date': today, 'rate': f'{rate:.2f}', 'timestamp': timestamp})
    except Exception:
        pass


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


def show_history(days=7):
    """Display recent exchange rates"""
    try:
        if not os.path.exists(HISTORY_FILE):
            print("Aucun historique disponible.")
            return

        print(f"\n{'='*50}")
        print(f"Historique EUR/JPY (derniers {days} jours)")
        print(f"{'='*50}")

        rates = []
        with open(HISTORY_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rates = list(reader)

        if rates:
            recent_rates = rates[-days:]
            for row in recent_rates:
                print(f"{row['date']}: 1 EUR = {row['rate']} JPY")
            print(f"{'='*50}\n")
        else:
            print("Aucune donnée d'historique.")
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique: {e}")


if __name__ == "__main__":
    rate = get_eur_jpy_rate()
    show_history(days=7)
