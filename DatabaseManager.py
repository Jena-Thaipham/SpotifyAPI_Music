import sqlite3
import logging
import pandas as pd
from typing import Dict
from pathlib import Path
import os

class DatabaseManager:
    def __init__(self, db_path: str = "spotify_db/spotify.db", schema_dir: str = "spotify_db/schema"):
        self.db_path = db_path
        self.schema_dir = schema_dir
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
        cursor.execute("PRAGMA foreign_keys = OFF")

        schema_dir_path = Path(self.schema_dir)
        sql_files = sorted(schema_dir_path.glob("*.sql"))

        for schema_file in sql_files:
            sql = self._load_schema_file(schema_file)
            cursor.executescript(sql)

        self.connection.commit()

    def save_data(self, dataframes: Dict[str, pd.DataFrame]) -> bool:
        if not self.connection:
            logging.error("Database connection not established")
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA foreign_keys = OFF")

            for table, df in dataframes.items():
                if df.empty:
                    logging.warning(f"Empty dataframe for table {table}")
                    continue

                if table == "playlists" and "tracks" in df.columns:
                    df = df.drop(columns=["tracks"])

                df = df.where(pd.notnull(df), None)
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['?'] * len(df.columns))

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                if not cursor.fetchone():
                    logging.error(f"Table {table} does not exist")
                    continue

                sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
                data_tuples = [tuple(x) for x in df.to_numpy()]

                try:
                    cursor.executemany(sql, data_tuples)
                    logging.info(f"Inserted/updated {len(data_tuples)} rows to {table}")
                except sqlite3.Error as e:
                    logging.error(f"Error inserting to {table}: {str(e)}")
                    logging.debug(f"Sample data: {data_tuples[:5]}")
                    raise

            self.connection.commit()
            logging.info("Data saved successfully")
            return True

        except Exception as e:
            self.connection.rollback()
            logging.exception("Failed to save data")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
