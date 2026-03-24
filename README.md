# AI Business Analyst Copilot

An AI-powered system that enables users to query business data using natural language and receive insights, analysis, and predictions.

---

## 🔍 Overview

This project simulates a real-world business analytics assistant where users can ask questions like:

- “Show revenue by category”
- “Which region performs best?”
- “Why is revenue low?”
- “Predict next 5 days revenue”

The system combines **SQL, Machine Learning, and LLMs** to deliver actionable business insights.

---

## ⚙️ Key Features

- 🔹 Natural Language → SQL query generation using LLMs  
- 🔹 Automated data analysis and insight generation  
- 🔹 Revenue forecasting using machine learning models  
- 🔹 Modular multi-agent architecture (SQL, Analysis, ML)  
- 🔹 Interactive UI built with Streamlit  

---

## 🧠 System Architecture

User Query  
→ Orchestrator  
→ Specialized Agents  

- **SQL Agent** → Converts natural language to SQL and retrieves data  
- **Analysis Agent** → Generates insights from data  
- **ML Agent** → Performs forecasting and predictions  

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **OpenAI (LLM)**
- **Streamlit**
- **SQLite**

---

## 📊 Sample Queries

Try asking:

- Show total revenue by category  
- Which region has highest sales?  
- Give insights on revenue trends  
- Predict next 5 days revenue  

---

## ▶️ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
