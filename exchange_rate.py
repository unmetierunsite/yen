#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and daily history
"""

import requests
from datetime import datetime
import json
import os
import sys

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.json'
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
                        save_history(rate)
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


def save_history(rate):
    """Save rate to daily history file"""
    try:
        history = load_history()
        today = datetime.now().strftime('%Y-%m-%d')

        history[today] = {
            'rate': rate,
            'timestamp': datetime.now().isoformat()
        }

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass


def load_history():
    """Load history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def display_history(days=None):
    """Display historical exchange rates"""
    history = load_history()

    if not history:
        print("Aucun historique disponible.")
        return

    # Sort by date
    sorted_dates = sorted(history.keys(), reverse=True)

    if days:
        sorted_dates = sorted_dates[:days]

    print(f"\n{'='*60}")
    print(f"Historique des taux EUR/JPY ({len(sorted_dates)} jours)")
    print(f"{'='*60}")

    for date in sorted_dates:
        rate = history[date]['rate']
        print(f"{date}: 1 EUR = {rate:.2f} JPY")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--history':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else None
            display_history(days)
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python exchange_rate.py          # Afficher le taux actuel")
            print("  python exchange_rate.py --history [N]  # Afficher l'historique (derniers N jours)")
    else:
        get_eur_jpy_rate()
