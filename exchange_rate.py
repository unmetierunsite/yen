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


def get_eur_jpy_rate(use_cache=True, save_history=True):
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
                        if save_history:
                            save_to_history(rate)
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
                if save_history:
                    save_to_history(cached_rate)
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        display_rate(FALLBACK_RATE)
        if save_history:
            save_to_history(FALLBACK_RATE)
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


def save_to_history(rate):
    """Save rate to daily history file"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        history = load_history()

        if not history:
            history = {}

        # Only save once per day
        if today not in history:
            history[today] = {
                'rate': rate,
                'timestamp': datetime.now().isoformat()
            }
            with open(HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)
    except Exception:
        pass


def load_history():
    """Load rate history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None


def display_history():
    """Display the exchange rate history"""
    history = load_history()

    if not history:
        print("Aucun historique disponible.")
        return

    print(f"\n{'='*60}")
    print("Historique des taux de change EUR/JPY")
    print(f"{'='*60}")
    print(f"{'Date':<12} | {'Taux':<10} | {'1 EUR =':<15}")
    print(f"{'-'*60}")

    for date in sorted(history.keys()):
        data = history[date]
        rate = data['rate']
        print(f"{date} | {rate:>8.2f} | {rate:.2f} JPY")

    print(f"{'='*60}\n")


def display_stats():
    """Display statistics about the exchange rate"""
    history = load_history()

    if not history or len(history) < 2:
        print("Pas assez de données pour calculer les statistiques.")
        return

    rates = [data['rate'] for data in history.values()]

    print(f"\n{'='*60}")
    print("Statistiques des taux de change EUR/JPY")
    print(f"{'='*60}")
    print(f"Nombre de jours suivis: {len(rates)}")
    print(f"Taux maximum: {max(rates):.2f} JPY")
    print(f"Taux minimum: {min(rates):.2f} JPY")
    print(f"Taux moyen: {sum(rates)/len(rates):.2f} JPY")
    print(f"Variation: {max(rates) - min(rates):.2f} JPY")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'history':
            display_history()
        elif sys.argv[1] == 'stats':
            display_stats()
        else:
            print("Usage: python exchange_rate.py [command]")
            print("Commands:")
            print("  (no command) - Show current rate and save to history")
            print("  history     - Display exchange rate history")
            print("  stats       - Display statistics")
    else:
        get_eur_jpy_rate()
