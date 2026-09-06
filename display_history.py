#!/usr/bin/env python3
"""
Display historical EUR/JPY exchange rates
"""

import json
import os
from datetime import datetime

DAILY_LOG_FILE = 'exchange_rate_daily.json'


def display_history():
    """Display all recorded daily exchange rates"""
    if not os.path.exists(DAILY_LOG_FILE):
        print("No exchange rate history found. Run exchange_rate.py first.")
        return

    try:
        with open(DAILY_LOG_FILE, 'r') as f:
            history = json.load(f)

        if not history:
            print("No exchange rate history found.")
            return

        print("\n" + "="*60)
        print("EUR/JPY EXCHANGE RATE HISTORY")
        print("="*60)

        dates = sorted(history.keys(), reverse=True)
        for date in dates:
            entry = history[date]
            rate = entry['rate']
            timestamp = entry['timestamp']
            print(f"{date}: 1 EUR = {rate:.2f} JPY")

        print("="*60 + "\n")

        if len(history) > 1:
            rates = [entry['rate'] for entry in history.values()]
            min_rate = min(rates)
            max_rate = max(rates)
            avg_rate = sum(rates) / len(rates)
            latest_rate = history[dates[0]]['rate']

            print(f"Taux minimum: {min_rate:.2f} JPY")
            print(f"Taux maximum: {max_rate:.2f} JPY")
            print(f"Taux moyen:   {avg_rate:.2f} JPY")
            print(f"Taux actuel:  {latest_rate:.2f} JPY\n")

    except Exception as e:
        print(f"Error reading history: {e}")


if __name__ == "__main__":
    display_history()
