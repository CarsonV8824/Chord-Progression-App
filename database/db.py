import os
import sqlite3
import sys
from pathlib import Path

class Database:
    def __init__(self):
        # Use user's home directory for database (works for .exe and script)
        app_data_dir = Path.home() / ".chord_progression_app"
        app_data_dir.mkdir(exist_ok=True)
        self.db_path = app_data_dir / "chord-progression-app.db"

        self.connection = sqlite3.connect(str(self.db_path))
        self.cursor = self.connection.cursor()
        self.__make_table()

    def __make_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chord (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                chord_progression TEXT    
                );
        """)
        self.connection.commit()
        
    def add_data(self, chord_progression:str):
        self.cursor.execute("""
            INSERT INTO chord (chord_progression) VALUES (?);
        """, (chord_progression,))
        self.connection.commit()

    def get_data(self):
        self.cursor.execute("""SELECT * FROM chord;""")
        data = self.cursor.fetchall()
        return data
    
    def delete_data_by_progression(self, chord_progression: str):
        self.cursor.execute("""
            DELETE FROM chord WHERE chord_progression = ?;
        """, (chord_progression,))
        self.connection.commit()

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.connection.close()
        except:
            pass