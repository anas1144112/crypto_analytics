from database import get_connection, release_connection
from psycopg2.extras import execute_batch

def load_data(data):
    conn = get_connection()
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO crypto_market (
        coin_id, symbol, name, current_price,
        market_cap, total_volume,
        price_change_24h, market_cap_rank,
        volatility_score, extracted_at
    )
    VALUES (
        %(coin_id)s, %(symbol)s, %(name)s, %(current_price)s,
        %(market_cap)s, %(total_volume)s,
        %(price_change_24h)s, %(market_cap_rank)s,
        %(volatility_score)s, %(extracted_at)s
    )
    ON CONFLICT (coin_id, extracted_at)
    DO NOTHING;
    """
    
    try:
        execute_batch(cur, insert_query, data)
        conn.commit()
        print(f"{len(data)} rows inserted.")
        
    except Exception as e:
        conn.rollback()
        print("Load Error:", e)
        
    finally:
        cur.close()
        release_connection(conn)