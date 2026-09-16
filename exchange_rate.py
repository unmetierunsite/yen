#!/usr/bin/env python3
"""
Script to track and display EUR/JPY exchange rate with daily history
"""

import requests
from datetime import datetime
import json
import os
import csv
from pathlib import Path

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.csv'
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
                        save_to_history(rate)
                        display_summary(rate)
                        return rate
            except Exception:
                continue

        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                print(f"\n{'='*60}")
                print("⚠️  Données en cache (connexion API échouée)")
                print(f"{'='*60}")
                save_to_history(cached_rate)
                display_summary(cached_rate)
                return cached_rate

        print(f"\n{'='*60}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*60}")
        save_to_history(FALLBACK_RATE)
        display_summary(FALLBACK_RATE)
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_summary(rate):
    """Display current rate and historical statistics"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"\nTaux de change EUR/JPY - {timestamp}")
    print(f"{'='*60}")
    print(f"1 EUR = {rate:.2f} JPY")
    print(f"{'='*60}")

    stats = get_history_stats()
    if stats:
        print("\n📊 Statistiques (derniers 30 jours):")
        print(f"   Moyenne: {stats['average']:.2f} JPY")
        print(f"   Min: {stats['min']:.2f} JPY (le {stats['min_date']})")
        print(f"   Max: {stats['max']:.2f} JPY (le {stats['max_date']})")
        print(f"   Jours enregistrés: {stats['count']}")
    print()


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


def save_to_history(rate):
    """Save daily rate to history CSV file"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        history_exists = os.path.exists(HISTORY_FILE)

        if history_exists:
            with open(HISTORY_FILE, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if rows and rows[-1][0] == today:
                rows[-1] = [today, f'{rate:.2f}', datetime.now().isoformat()]
            else:
                rows.append([today, f'{rate:.2f}', datetime.now().isoformat()])

            with open(HISTORY_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        else:
            with open(HISTORY_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'rate', 'timestamp'])
                writer.writerow([today, f'{rate:.2f}', datetime.now().isoformat()])
    except Exception:
        pass


def get_history_stats():
    """Get statistics from history file"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return None

        rates = []
        dates = []

        with open(HISTORY_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    rates.append(float(row[1]))
                    dates.append(row[0])

        if not rates:
            return None

        min_idx = rates.index(min(rates))
        max_idx = rates.index(max(rates))

        return {
            'average': sum(rates) / len(rates),
            'min': min(rates),
            'max': max(rates),
            'min_date': dates[min_idx],
            'max_date': dates[max_idx],
            'count': len(rates)
        }
    except Exception:
        pass
    return None


if __name__ == "__main__":
    get_eur_jpy_rate()
