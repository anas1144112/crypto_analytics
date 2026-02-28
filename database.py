import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "database": "crypto_db",
    "user": "postgres",
    "password": "anas1409",
    "port": 5432
}

connection_pool = pool.SimpleConnectionPool(
    1, 10, **DB_CONFIG
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS crypto_market (
            id SERIAL PRIMARY KEY,
            coin_id TEXT,
            symbol TEXT,
            name TEXT,
            current_price FLOAT,
            market_cap BIGINT,
            total_volume BIGINT,
            price_change_24h FLOAT,
            market_cap_rank INTEGER,
            volatility_score FLOAT,
            extracted_at TIMESTAMP,
            UNIQUE (coin_id, extracted_at)
        );
        """)
        
        cur.execute("CREATE INDEX IF NOT EXISTS idx_coin_id ON crypto_market(coin_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_extracted_at ON crypto_market(extracted_at);")
        
        conn.commit()
        print("Table created successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        release_connection(conn)