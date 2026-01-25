import os
import sqlite3
import sys

class Database:
    def __init__(self):
        base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, "database")
        os.makedirs(db_dir, exist_ok=True)  
        db_path = os.path.join(db_dir, "chord-progression-app.db")

        self.connection = sqlite3.connect(db_path)
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
    
    def __del__(self):
        self.connection.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

if __name__ == "__main__":
    test = Database()
    test.add_data("testing")
    print(test.get_data)