import requests
import json
import os
from datetime import datetime

def fetch_crypto_data():
    """Fetches top 100 cryptocurrencies by market cap from CoinGecko"""
    print("[extract] Fetching live crypto data from CoinGecko...")
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Save locally first
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/raw/crypto_market_{timestamp}.json"
    
    with open(filepath, "w") as f:
        json.dump(data, f)
        
    print(f"[extract] ✅ Saved {len(data)} coins to {filepath}")
    return filepath

if __name__ == "__main__":
    fetch_crypto_data()
