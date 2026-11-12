import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(ROOT_DIR / ".env")

DB_URL = os.getenv("DATABASE_URL")

print(f"DB_URL: {DB_URL}")

conn = None

try:
    if not DB_URL:
        raise Exception("DATABASE_URL not found in .env file")

    conn = psycopg2.connect(DB_URL)

    print("✅ Database connection successful")

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            prompt TEXT,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    print("✅ Tables created successfully")

except Exception as error:
    print(f"❌ Error: {error}")

finally:
    if conn is not None:
        conn.close()
        print("✅ Database connection closed")
