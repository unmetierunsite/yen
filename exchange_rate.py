#!/usr/bin/env python3
"""
Script to display current EUR/JPY exchange rate and track daily history
"""

import requests
from datetime import datetime
import json
import os

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
                        display_rate(rate, is_live=True)
                        return rate
            except Exception:
                continue

        # If API fails, try cache
        if use_cache:
            cached_rate = load_cache()
            if cached_rate:
                save_history(cached_rate)
                print(f"\n{'='*50}")
                print("⚠️  Données en cache (connexion API échouée)")
                print(f"{'='*50}")
                display_rate(cached_rate, is_live=False)
                show_history()
                return cached_rate

        # Last resort: use fallback
        print(f"\n{'='*50}")
        print("⚠️  Taux de change approximatif (valeur par défaut)")
        print(f"{'='*50}")
        save_history(FALLBACK_RATE)
        display_rate(FALLBACK_RATE, is_live=False)
        show_history()
        return FALLBACK_RATE

    except Exception as e:
        print(f"Erreur: {e}")
        return None


def display_rate(rate, is_live=True):
    """Display the exchange rate"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "✅ EN DIRECT" if is_live else "📊 DONNÉES MISES EN CACHE"
    print(f"Taux de change EUR/JPY - {timestamp} ({status})")
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
    """Save rate to daily history"""
    try:
        history = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)

        today = datetime.now().strftime('%Y-%m-%d')
        if today not in history:
            history[today] = []

        entry = {
            'rate': rate,
            'timestamp': datetime.now().isoformat()
        }

        if not history[today] or history[today][-1]['rate'] != rate:
            history[today].append(entry)

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass


def show_history():
    """Display exchange rate history statistics"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return

        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)

        if not history:
            return

        all_rates = []
        for date, entries in sorted(history.items()):
            if entries:
                all_rates.append(entries[-1]['rate'])

        if len(all_rates) > 1:
            print("📈 Historique:")
            print(f"{'='*50}")
            print(f"Minimum: {min(all_rates):.2f} JPY")
            print(f"Maximum: {max(all_rates):.2f} JPY")
            print(f"Moyenne: {sum(all_rates)/len(all_rates):.2f} JPY")
            print(f"Jours suivis: {len(all_rates)}")
            print(f"{'='*50}\n")
    except Exception:
        pass


if __name__ == "__main__":
    get_eur_jpy_rate()
