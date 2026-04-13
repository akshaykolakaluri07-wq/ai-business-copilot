import sqlite3
import pandas as pd

DB_PATH = "sales.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_csv("data/sales.csv", encoding="utf-8")

        if df.empty:
            raise ValueError("CSV loaded but empty")

        df.columns = [col.strip().lower() for col in df.columns]

        df.to_sql("sales", conn, if_exists="replace", index=False)

    except Exception as e:
        print("DB INIT ERROR:", str(e))
        raise e

    finally:
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
