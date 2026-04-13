def analyze(df):
    if isinstance(df, str):
        return df

    insights = {}
    insights["total_revenue"] = df["revenue"].sum()
    insights["avg_revenue"] = df["revenue"].mean()
    insights["top_category"] = df.groupby("category")["revenue"].sum().idxmax()

    return insights
