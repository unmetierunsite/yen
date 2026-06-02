#!/usr/bin/env python3
"""
Script to track daily EUR/JPY exchange rate history
"""

import requests
from datetime import datetime
import json
import os

CACHE_FILE = 'exchange_rate_cache.json'
HISTORY_FILE = 'exchange_rate_history.json'
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
                        rate = data['rates']['JPY']
                    elif 'rates' in data and 'JPY' in data['rates']:
                        rate = data['rates']['JPY']

                    if rate:
                        save_cache(rate)
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
    """Display the current exchange rate"""
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
    """Save daily rate to history file"""
    try:
        history = load_history()
        today = datetime.now().strftime('%Y-%m-%d')

        if today in history:
            history[today].append({
                'rate': rate,
                'timestamp': datetime.now().isoformat()
            })
        else:
            history[today] = [{
                'rate': rate,
                'timestamp': datetime.now().isoformat()
            }]

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


def show_history():
    """Display exchange rate history"""
    history = load_history()
    if not history:
        print("Aucun historique disponible")
        return

    print(f"\n{'='*60}")
    print("HISTORIQUE DU TAUX EUR/JPY")
    print(f"{'='*60}")

    rates_by_day = []
    for date in sorted(history.keys()):
        daily_rates = history[date]
        avg_rate = sum(r['rate'] for r in daily_rates) / len(daily_rates)
        min_rate = min(r['rate'] for r in daily_rates)
        max_rate = max(r['rate'] for r in daily_rates)

        rates_by_day.append({
            'date': date,
            'avg': avg_rate,
            'min': min_rate,
            'max': max_rate,
            'count': len(daily_rates)
        })

        print(f"\n{date}:")
        print(f"  Moyenne: {avg_rate:.2f} JPY")
        print(f"  Min: {min_rate:.2f} JPY | Max: {max_rate:.2f} JPY")
        print(f"  Observations: {len(daily_rates)}")

    # Show overall statistics
    if rates_by_day:
        all_rates = [r['avg'] for r in rates_by_day]
        print(f"\n{'='*60}")
        print("STATISTIQUES GLOBALES")
        print(f"{'='*60}")
        print(f"Jours suivis: {len(rates_by_day)}")
        print(f"Taux moyen: {sum(all_rates)/len(all_rates):.2f} JPY")
        print(f"Taux minimum: {min(all_rates):.2f} JPY")
        print(f"Taux maximum: {max(all_rates):.2f} JPY")

        # Calculate trend
        if len(all_rates) > 1:
            first_rate = all_rates[0]
            last_rate = all_rates[-1]
            change = last_rate - first_rate
            percent_change = (change / first_rate) * 100
            trend = "📈 À la hausse" if change > 0 else "📉 À la baisse"
            print(f"\nTendance: {trend}")
            print(f"Variation: {change:+.2f} JPY ({percent_change:+.2f}%)")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--history':
        show_history()
    else:
        get_eur_jpy_rate()
