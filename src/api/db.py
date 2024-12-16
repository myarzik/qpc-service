import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self._create_cities_table()
        self._create_games_table()
        self._create_teams_table()  # Создаем таблицу для команд

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

    def _create_games_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            datetime TEXT,
            price INTEGER,
            city_id INTEGER,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        )
        """)

    def _create_teams_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT,
            captain_name TEXT,
            email TEXT,
            phone TEXT,
            city_id INTEGER,
            telegram_group_id TEXT,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        )
        """)

    def update_cities(self, city_id, city_title, map_type):
        with self.connection as conn:
            conn.execute("""
            INSERT OR REPLACE INTO cities (id, title, map_type)
            VALUES (?, ?, ?)
            """, (city_id, city_title, map_type))

    def update_games(self, game_id, title, description, datetime, price, city_id):
        with self.connection as conn:
            conn.execute("""
            INSERT OR REPLACE INTO games (id, title, description, datetime, price, city_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (game_id, title, description, datetime, price, city_id))

    def update_teams(self, team_id, name, captain_name, email, phone, city_id, telegram_group_id):
        with self.connection as conn:
            conn.execute("""
            INSERT OR REPLACE INTO teams (id, name, captain_name, email, phone, city_id, telegram_group_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (team_id, name, captain_name, email, phone, city_id, telegram_group_id))