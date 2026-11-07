#!/usr/bin/env python3
"""
Script to track daily EUR/JPY exchange rate
"""

import requests
from datetime import datetime
import json
import os

CACHE_FILE = 'exchange_rate_cache.json'
TRACKING_FILE = 'exchange_rate_history.json'
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


def track_daily_rate():
    """Fetch and store the daily exchange rate"""
    rate = get_eur_jpy_rate()

    if rate:
        today = datetime.now().strftime('%Y-%m-%d')

        history = {}
        if os.path.exists(TRACKING_FILE):
            try:
                with open(TRACKING_FILE, 'r') as f:
                    history = json.load(f)
            except Exception:
                pass

        history[today] = {
            'rate': rate,
            'timestamp': datetime.now().isoformat()
        }

        try:
            with open(TRACKING_FILE, 'w') as f:
                json.dump(history, f, indent=2)
            print(f"✓ Taux enregistré pour {today}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement: {e}")

        return rate
    return None


def display_history():
    """Display exchange rate history"""
    if not os.path.exists(TRACKING_FILE):
        print("Aucun historique disponible")
        return

    try:
        with open(TRACKING_FILE, 'r') as f:
            history = json.load(f)

        print(f"\n{'='*50}")
        print("Historique EUR/JPY")
        print(f"{'='*50}")

        for date in sorted(history.keys()):
            rate = history[date]['rate']
            print(f"{date}: 1 EUR = {rate:.2f} JPY")

        if history:
            rates = [h['rate'] for h in history.values()]
            print(f"{'='*50}")
            print(f"Min: {min(rates):.2f} JPY | Max: {max(rates):.2f} JPY | Moy: {sum(rates)/len(rates):.2f} JPY")
            print(f"{'='*50}\n")
    except Exception as e:
        print(f"Erreur lors de la lecture de l'historique: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--history':
        display_history()
    else:
        track_daily_rate()
