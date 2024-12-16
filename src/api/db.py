import sqlite3


class TeamNotFoundError(Exception):
    """Team not found."""
    pass


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

    def create_team(self, name, captain_name, email, phone, city_id, telegram_group_id):
        with self.connection as conn:
            conn.execute("""
            INSERT INTO teams (name, captain_name, email, phone, city_id, telegram_group_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, captain_name, email, phone, city_id, telegram_group_id))
            print(f"Team '{name}' created successfully!")

    def read_team(self, team_id):
        self.cursor.execute("""
        SELECT * FROM teams WHERE id = ?
        """, (team_id,))
        team = self.cursor.fetchone()
        if not team:
            raise TeamNotFoundError(f"Team with ID {team_id} not found.")
        return {
            "id": team[0],
            "name": team[1],
            "captain_name": team[2],
            "email": team[3],
            "phone": team[4],
            "city_id": team[5],
            "telegram_group_id": team[6]
        }

    def update_team(self, team_id, name=None, captain_name=None, email=None, phone=None, city_id=None, telegram_group_id=None):
        team = self.read_team(team_id)

        updated_values = {
            "name": name if name else team["name"],
            "captain_name": captain_name if captain_name else team["captain_name"],
            "email": email if email else team["email"],
            "phone": phone if phone else team["phone"],
            "city_id": city_id if city_id else team["city_id"],
            "telegram_group_id": telegram_group_id if telegram_group_id else team["telegram_group_id"]
        }

        with self.connection as conn:
            conn.execute("""
            UPDATE teams
            SET name = ?, captain_name = ?, email = ?, phone = ?, city_id = ?, telegram_group_id = ?
            WHERE id = ?
            """, (updated_values["name"], updated_values["captain_name"], updated_values["email"],
                  updated_values["phone"], updated_values["city_id"], updated_values["telegram_group_id"], team_id))
            print(f"Team with ID {team_id} updated successfully!")

    def delete_team(self, team_id):
        if not self.read_team(team_id):
            raise TeamNotFoundError(f"Team with ID {team_id} not found.")
        with self.connection as conn:
            conn.execute("""
            DELETE FROM teams WHERE id = ?
            """, (team_id,))
            print(f"Team with ID {team_id} deleted successfully!")

    def list_teams(self):
        self.cursor.execute("""
        SELECT * FROM teams
        """)
        teams = self.cursor.fetchall()
        return [
            {
                "id": team[0],
                "name": team[1],
                "captain_name": team[2],
                "email": team[3],
                "phone": team[4],
                "city_id": team[5],
                "telegram_group_id": team[6]
            }
            for team in teams
        ]

if __name__ == "__main__":
    with Database() as db:
        db.create_team("Team Alpha", "Alice", "alice@example.com", "+1234567890", 1, "telegram-group-123")

        try:
            team = db.read_team(1)
            print("Read Team:", team)
        except TeamNotFoundError as e:
            print(e)

        try:
            db.read_team(999)
        except TeamNotFoundError as e:
            print(e)

        try:
            db.delete_team(999)
        except TeamNotFoundError as e:
            print(e)

        try:
            db.update_team(1, captain_name="Alice Smith", email="newalice@example.com")
            updated_team = db.read_team(1)
            print("Updated Team:", updated_team)
        except TeamNotFoundError as e:
            print(e)