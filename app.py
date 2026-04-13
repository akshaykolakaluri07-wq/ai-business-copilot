import streamlit as st
from db.database import init_db
from agents.langgraph_orchestrator import handle_query

st.set_page_config(page_title="AI Business Copilot")

init_db()

st.title("📊 AI Business Analyst Copilot")

query = st.text_input("Ask a business question:")

if st.button("Run"):
    if query:
        result = handle_query(query)

        if result is None:
            st.error("No result returned")

        elif isinstance(result, str):
            st.write(result)

        else:
            st.dataframe(result)  # 🔥 force dataframe display

    else:
        st.warning("Enter a query")
