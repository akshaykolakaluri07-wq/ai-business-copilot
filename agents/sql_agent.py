from utils.llm import ask_llm
from db.database import run_query
import pandas as pd

SCHEMA = """
Table: sales
Columns:
date (text), category (text), revenue (int), orders (int), region (text)
"""

# 🔹 Clean LLM output
def clean_sql(sql):
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

    return sql.strip()


# 🔹 Validate SQL (safe queries only)
def is_valid_sql(sql):
    sql_lower = sql.lower()

    return (
        sql_lower.startswith("select") and
        "drop" not in sql_lower and
        "delete" not in sql_lower and
        "update" not in sql_lower and
        "insert" not in sql_lower
    )


# 🔹 Generate SQL using LLM
def generate_sql(user_query):
    prompt = f"""
You are a SQL expert.

{SCHEMA}

Rules:
- Return ONLY a SQL query
- Do NOT use markdown or backticks
- Only generate SELECT queries
- Use correct column names
- Do not hallucinate columns

Question: {user_query}
"""
    return ask_llm(prompt)


# 🔥 Retry logic (VERY IMPORTANT)
def generate_valid_sql(user_query, retries=2):
    for _ in range(retries):
        sql = generate_sql(user_query)
        sql = clean_sql(sql)

        if is_valid_sql(sql):
            return sql

    return None


# 🔹 Main agent
def sql_agent(user_query):

    sql = generate_valid_sql(user_query)

    if sql is None:
        return {"error": "Failed to generate valid SQL"}

    print("FINAL SQL:", sql)

    try:
        result = run_query(sql)

        # 🔥 Ensure always DataFrame
        if isinstance(result, pd.DataFrame):
            return result
        else:
            return {"error": str(result)}

    except Exception as e:
        return {"error": str(e)}
