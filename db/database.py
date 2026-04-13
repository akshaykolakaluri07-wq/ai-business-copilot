import sqlite3
import pandas as pd
import os

# 🔹 Base directory (important for Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 Correct DB path
DB_PATH = os.path.join(BASE_DIR, "sales.db")

# 🔹 Correct CSV path
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")


def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)

        df = pd.read_csv(DATA_PATH)

        df.to_sql("sales", conn, if_exists="replace", index=False)

        conn.close()
        print("DB initialized successfully")

    except Exception as e:
        print("DB INIT ERROR:", e)


def run_query(query):
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        return f"SQL ERROR: {str(e)}"

    finally:
        conn.close()
