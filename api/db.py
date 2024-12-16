import json
import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self._create_cities_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def _create_cities_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            title TEXT,
            map_type TEXT
        )
        """)

    def update_cities(self, city_id, city_title, map_type):
        with self.connection as conn:
            conn.execute("""
            INSERT OR REPLACE INTO cities (id, title, map_type)
            VALUES (?, ?, ?)
            """, (city_id, city_title, map_type))
