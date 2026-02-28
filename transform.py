from datetime import datetime

def transform_data(raw_data):
    transformed = []
    
    for coin in raw_data:
        try:
            if coin["current_price"] is None:
                continue
                
            volatility_score = abs(coin["price_change_percentage_24h"] or 0) * (coin["total_volume"] or 0)
            
            transformed.append({
                "coin_id": coin["id"],
                "symbol": coin["symbol"],
                "name": coin["name"],
                "current_price": float(coin["current_price"]),
                "market_cap": int(coin["market_cap"] or 0),
                "total_volume": int(coin["total_volume"] or 0),
                "price_change_24h": float(coin["price_change_percentage_24h"] or 0),
                "market_cap_rank": int(coin["market_cap_rank"] or 0),
                "volatility_score": volatility_score,
                "extracted_at": datetime.now()
            })
        except Exception as e:
            print("Transform error:", e)
    
    return transformed