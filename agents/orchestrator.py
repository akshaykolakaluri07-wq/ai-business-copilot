import re
from agents.sql_agent import sql_agent
from agents.analysis_agent import analyze
from agents.ml_agent import forecast


def route_query(query):
    q = query.lower()

    if "predict" in q or "forecast" in q:
        return "ml"
    elif "why" in q or "analysis" in q:
        return "analysis"
    else:
        return "sql"


def extract_days(query):
    q = query.lower()

    if "week" in q:
        return 7
    if "month" in q:
        return 30

    match = re.search(r"(\d+)", q)
    if match:
        return int(match.group(1))

    return 5  # default


def handle_query(query):
    route = route_query(query)

    if route == "ml":
        df = sql_agent("SELECT * FROM sales")

        n_days = extract_days(query)
        return forecast(df, n_days=n_days)

    elif route == "analysis":
        df = sql_agent("SELECT * FROM sales")
        return analyze(df)

    else:
        return sql_agent(query) 
