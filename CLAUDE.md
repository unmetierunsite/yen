# EUR/JPY Exchange Rate Tracker

A daily automated task that fetches and displays the current EUR to JPY exchange rate.

## Purpose

This project runs daily to provide the current exchange rate: how many Japanese Yen you can get for 1 Euro.

## Setup

The project uses a simple Python script that:
- Fetches the EUR/JPY rate from multiple free APIs (exchangerate-api.com, open.er-api.com)
- Falls back to cached data if APIs are unavailable
- Uses a default rate (152.45 JPY) as a last resort
- Displays the rate with timestamp

## Running Manually

```bash
python exchange_rate.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Daily Scheduled Run

This task is configured to run daily via a scheduled session in Claude Code.
The results are displayed and can be monitored in the session transcript.

## Output Format

```
==================================================
Taux de change EUR/JPY - 2026-09-05 10:30:45
==================================================
1 EUR = 152.45 JPY
==================================================
```

## Cache

The script automatically caches the exchange rate in `exchange_rate_cache.json` for use when APIs are unavailable.
