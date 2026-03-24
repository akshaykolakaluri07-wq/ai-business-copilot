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

def handle_query(query):
    route = route_query(query)

    if route == "ml":
        df = sql_agent("SELECT * FROM sales")
        return forecast(df)

    elif route == "analysis":
        df = sql_agent("SELECT * FROM sales")
        return analyze(df)

    else:
        return sql_agent(query)
