def analyze(df):
    # 🔹 Handle errors from SQL agent
    if isinstance(df, dict) and "error" in df:
        return f"Error in data: {df['error']}"

    # 🔹 Handle string fallback
    if isinstance(df, str):
        return df

    # 🔹 Handle empty dataframe
    if df is None or df.empty:
        return "No data available for analysis"

    try:
        total_revenue = df["revenue"].sum()
        avg_revenue = df["revenue"].mean()
        top_category = df.groupby("category")["revenue"].sum().idxmax()

        # 🔥 Clean formatted output
        result = f"""
📊 Business Insights:

- Total Revenue: {total_revenue}
- Average Revenue: {avg_revenue:.2f}
- Top Category: {top_category}
"""

        return result

    except Exception as e:
        return f"Analysis Error: {str(e)}"
