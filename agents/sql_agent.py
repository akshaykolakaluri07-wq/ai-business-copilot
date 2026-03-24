from utils.llm import ask_llm
from db.database import run_query

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
- Do NOT explain anything
- Only generate SELECT queries

Question: {user_query}
"""
    return ask_llm(prompt)


# 🔹 Main agent
def sql_agent(user_query):
    sql = generate_sql(user_query)

    print("RAW SQL:", sql)  # debug

    sql = clean_sql(sql)

    if not is_valid_sql(sql):
        return f"❌ Invalid or unsafe SQL generated:\n{sql}"

    try:
        result = run_query(sql)
        return result
    except Exception as e:
        return f"❌ SQL Execution Error:\n{str(e)}\n\nQuery:\n{sql}"
