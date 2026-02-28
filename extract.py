import requests
import json
from datetime import datetime

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

def extract_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": "false"
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Save raw JSON
        with open(f"logs/raw_{datetime.now().timestamp()}.json", "w") as f:
            json.dump(data, f)
        
        return data
    
    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return []