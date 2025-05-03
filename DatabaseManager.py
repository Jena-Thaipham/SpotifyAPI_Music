import sqlite3
import logging
import pandas as pd
from pathlib import Path
import os

class DatabaseManager:
    def __init__(self, db_path: str = "spotify_db/spotify.db", schema_dir: str = "spotify_db/schema"):
        self.db_path = db_path
        self.schema_dir = Path(schema_dir)
        self.connection = None
        self._initialize_database()

    def _load_schema_file(self, filename: str) -> str:
        schema_path = Path(self.schema_dir) / filename
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _initialize_database(self):
        if Path(self.db_path).exists():
            os.remove(self.db_path)

        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        schema_dir_path = Path(self.schema_dir)
        sql_files = sorted(schema_dir_path.glob("*.sql"))

        for schema_file in sql_files:
            sql = self._load_schema_file(schema_file.name)
            cursor.executescript(sql)

        self.connection.commit()

    def save_table(self, table: str, df: pd.DataFrame) -> bool:
        if not self.connection:
            logging.error("Database connection not established.")
            return False

        if df.empty:
            logging.warning(f"Empty dataframe for table {table}.")
            return False

        try:
            if table == "playlists" and "tracks" in df.columns:
                df = df.drop(columns=["tracks"])

            df = df.where(pd.notnull(df), None)  
         
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                logging.error(f"Table {table} does not exist in database.")
                return False

            df.to_sql(table, self.connection, if_exists='replace', index=False)
            logging.info(f"Inserted/updated {len(df)} rows into {table}.")
            return True

        except Exception as e:
            logging.error(f"Failed to insert data into {table}: {str(e)}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
