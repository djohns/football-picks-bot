import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            league TEXT,
            home_team TEXT,
            away_team TEXT,
            market TEXT,
            model_probability FLOAT,
            market_odds FLOAT,
            expected_value FLOAT,
            match_date TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_prediction(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions (
            league,
            home_team,
            away_team,
            market,
            model_probability,
            market_odds,
            expected_value,
            match_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """, data)

    conn.commit()
    cur.close()
    conn.close()
