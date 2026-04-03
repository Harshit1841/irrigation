"""
Seed ALL local plant data to Render PostgreSQL.
Extracts data from local irrigation.db and uploads to remote PostgreSQL.
"""

import os
import sqlite3

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./irrigation.db")

# Normalize for sync SQLAlchemy (use psycopg2 driver)
if DB_URL.startswith("postgresql+asyncpg"):
    DB_URL = DB_URL.replace("postgresql+asyncpg", "postgresql+psycopg2", 1)
elif DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


def seed_all_local_plants():
    local_db = (
        "C:\\Users\\mukul\\Downloads\\vibes xcg1234\\vibe xcg irrigation\\irrigation.db"
    )

    print(f"Reading from local database: {local_db}")
    conn = sqlite3.connect(local_db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT name, category, moisture_min, moisture_max, ideal_moisture, temp_min, temp_max, humidity_min, humidity_max, avg_moisture_decay_per_hour, description FROM plant_profiles"
    )
    rows = cur.fetchall()
    print(f"Found {len(rows)} plants in local database")

    # Seed to remote DB
    print(f"Seeding to: {DB_URL}")
    with engine.connect() as remote_conn:
        inserted = 0
        skipped = 0

        for row in rows:
            try:
                remote_conn.execute(
                    text("""
                    INSERT INTO plant_profiles
                    (name, category, moisture_min, moisture_max, ideal_moisture,
                     temp_min, temp_max, humidity_min, humidity_max,
                     avg_moisture_decay_per_hour, description, created_at)
                    VALUES (:name, :category, :moisture_min, :moisture_max, :ideal_moisture,
                            :temp_min, :temp_max, :humidity_min, :humidity_max,
                            :decay, :description, NOW())
                    ON CONFLICT (name) DO NOTHING
                """),
                    {
                        "name": row[0],
                        "category": row[1],
                        "moisture_min": row[2],
                        "moisture_max": row[3],
                        "ideal_moisture": row[4],
                        "temp_min": row[5],
                        "temp_max": row[6],
                        "humidity_min": row[7],
                        "humidity_max": row[8],
                        "decay": row[9],
                        "description": row[10],
                    },
                )
                inserted += 1
            except Exception as e:
                print(f"  Error: {e}")
                skipped += 1

        remote_conn.commit()

    conn.close()
    print(f"\nDone! Inserted: {inserted}, Skipped (duplicate/error): {skipped}")


if __name__ == "__main__":
    seed_all_local_plants()
