import sqlite3
import pandas as pd
from tabulate import tabulate

def get_database_summary(db_path="spotify_db/spotify.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)['name'].tolist()
    
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return

    summary_data = []
    column_stats = []
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        row_count = cursor.fetchone()[0]
        
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        col_count = len(columns)
        
        summary_data.append([table, row_count, col_count])
        
        if row_count > 0:
            df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1;", conn)
            sample_data = df.iloc[0].to_dict()
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                sample_value = str(sample_data.get(col_name, ''))[:50]
                column_stats.append([table, col_name, col_type, sample_value])
    
    print("\nDATABASE SUMMARY")
    print(tabulate(summary_data, 
                 headers=["Table", "Rows", "Columns"],
                 tablefmt="grid",
                 numalign="right"))
    
    print("\nCOLUMN DETAILS (First Row Samples)")
    print(tabulate(column_stats,
                 headers=["Table", "Column", "Type", "Sample Value"],
                 tablefmt="grid",
                 maxcolwidths=[None, None, None, 50]))
    
    print("\nBASIC STATISTICS")
    for table in tables:
        try:
            df = pd.read_sql(f"SELECT * FROM {table};", conn)
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                print(f"\n{table} - Numeric Columns Statistics:")
                print(df[numeric_cols].describe().to_markdown(tablefmt="grid"))
        except Exception as e:
            print(f"Could not describe table '{table}': {e}")

    conn.close()

if __name__ == "__main__":
    get_database_summary()
