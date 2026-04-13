import sqlite3
import pandas as pd

DB_PATH = "sales.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv("data/sales.csv")
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        return str(e)
    finally:
        conn.close()
