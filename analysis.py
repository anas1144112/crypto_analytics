from database import get_connection, release_connection

def execute_query(query):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        release_connection(conn)
        
def top_5_gainers():
    query = """
    SELECT name, price_change_24h
    FROM crypto_market
    WHERE extracted_at = (
        SELECT MAX(extracted_at)
        FROM crypto_market
    )
    ORDER BY price_change_24h DESC
    LIMIT 5;
    """
    return execute_query(query)


def top_5_market_cap():
    query = """
    SELECT name, market_cap
    FROM crypto_market
    WHERE extracted_at = (
        SELECT MAX(extracted_at)
        FROM crypto_market
    )
    ORDER BY market_cap DESC
    LIMIT 5;
    """
    return execute_query(query)


def average_market_cap():
    query = """
    SELECT AVG(market_cap)
    FROM crypto_market
    WHERE extracted_at = (
        SELECT MAX(extracted_at)
        FROM crypto_market
    );
    """
    return execute_query(query)

def total_market_value():
    query = """
    SELECT SUM(market_cap)
    FROM crypto_market
    WHERE extracted_at = (
        SELECT MAX(extracted_at)
        FROM crypto_market
    );
    """
    return execute_query(query)


def volatility_ranking():
    query = """
    SELECT name, volatility_score
    FROM crypto_market
    WHERE extracted_at = (
        SELECT MAX(extracted_at)
        FROM crypto_market
    )
    ORDER BY volatility_score DESC
    LIMIT 10;
    """
    return execute_query(query)