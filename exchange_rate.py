#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and maintain daily log
"""

import requests
from datetime import datetime
import json
import os
import csv

CACHE_FILE = 'exchange_rate_cache.json'
DAILY_LOG_FILE = 'exchange_rate_daily.csv'
FALLBACK_RATE = 152.45


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


def log_daily_rate(rate):
    """Log the daily exchange rate to CSV file"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        file_exists = os.path.exists(DAILY_LOG_FILE)

        with open(DAILY_LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Rate (JPY per EUR)', 'Time'])

            current_time = datetime.now().strftime('%H:%M:%S')
            writer.writerow([today, f'{rate:.2f}', current_time])
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du log: {e}")


def show_weekly_stats():
    """Show exchange rate statistics for the past week"""
    try:
        if not os.path.exists(DAILY_LOG_FILE):
            return

        rates = []
        with open(DAILY_LOG_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    rates.append(float(row['Rate (JPY per EUR)']))
                except (ValueError, KeyError):
                    continue

        if len(rates) > 0:
            print(f"\n{'='*50}")
            print("📊 Statistiques des 7 derniers jours")
            print(f"{'='*50}")
            print(f"Min: {min(rates):.2f} JPY")
            print(f"Max: {max(rates):.2f} JPY")
            print(f"Moyenne: {sum(rates)/len(rates):.2f} JPY")
            print(f"Enregistrements: {len(rates)}")
            print(f"{'='*50}\n")
    except Exception:
        pass


if __name__ == "__main__":
    rate = get_eur_jpy_rate()
    if rate:
        log_daily_rate(rate)
        show_weekly_stats()
