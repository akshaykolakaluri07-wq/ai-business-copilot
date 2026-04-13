from langgraph.graph import StateGraph
from typing import TypedDict
import re

from agents.sql_agent import sql_agent
from agents.analysis_agent import analyze
from agents.ml_agent import forecast


# 🔹 State definition
class AgentState(TypedDict):
    query: str
    route: str
    data: any
    result: any


# 🔹 Route logic (your existing logic)
def route_query(state: AgentState):
    q = state["query"].lower()

    if "predict" in q or "forecast" in q:
        return {"route": "ml"}
    elif "why" in q or "analysis" in q:
        return {"route": "analysis"}
    else:
        return {"route": "sql"}


# 🔹 Extract days (unchanged)
def extract_days(query):
    q = query.lower()

    if "week" in q:
        return 7
    if "month" in q:
        return 30

    match = re.search(r"(\d+)", q)
    if match:
        return int(match.group(1))

    return 5


# 🔹 SQL Node
def sql_node(state: AgentState):
    print("Running SQL Node...")
    df = sql_agent("SELECT * FROM sales")
    return {"data": df}


# 🔹 Direct SQL Node (for normal queries)
def direct_sql_node(state: AgentState):
    print("Running Direct SQL Query...")
    result = sql_agent(state["query"])
    return {"result": result}


# 🔹 Analysis Node
def analysis_node(state: AgentState):
    print("Running Analysis Node...")
    result = analyze(state["data"])
    return {"result": result}


# 🔹 ML Node
def ml_node(state: AgentState):
    print("Running ML Node...")
    n_days = extract_days(state["query"])
    result = forecast(state["data"], n_days=n_days)
    return {"result": result}


# 🔹 Router (LangGraph conditional edge)
def router(state: AgentState):
    return state["route"]


# 🔹 Build Graph
def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("route", route_query)
    graph.add_node("sql", sql_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("ml", ml_node)
    graph.add_node("direct_sql", direct_sql_node)

    # Entry
    graph.set_entry_point("route")

    # Routing
    graph.add_conditional_edges(
        "route",
        router,
        {
            "sql": "direct_sql",
            "analysis": "sql",
            "ml": "sql"
        }
    )

    # After SQL → go to analysis or ML
    graph.add_conditional_edges(
        "sql",
        router,
        {
            "analysis": "analysis",
            "ml": "ml"
        }
    )

    # End nodes
    graph.set_finish_point("analysis")
    graph.set_finish_point("ml")
    graph.set_finish_point("direct_sql")

    return graph.compile()


# 🔹 App instance
app = build_graph()


# 🔹 Public function (same as before)
def handle_query(query: str):
    result = app.invoke({"query": query})
    return result["result"]
