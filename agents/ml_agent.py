import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast(df, n_days=5):

    # 🔹 Handle SQL errors
    if isinstance(df, dict) and "error" in df:
        return f"Error in data: {df['error']}"

    # 🔹 Handle string fallback
    if isinstance(df, str):
        return df

    # 🔹 Handle empty data
    if df is None or df.empty:
        return "No data available for forecasting"

    try:
        # 🔹 Work on copy (important)
        df = df.copy()

        # 🔹 Ensure required columns
        if "date" not in df.columns or "revenue" not in df.columns:
            return "Required columns (date, revenue) missing"

        # 🔹 Convert date
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # 🔹 Feature engineering
        df["day"] = df["date"].dt.dayofyear

        X = df[["day"]]
        y = df["revenue"]

        # 🔹 Train model
        model = LinearRegression()
        model.fit(X, y)

        # 🔹 Get last date
        last_date = df["date"].max()

        # 🔹 Generate future dates
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=n_days
        )

        future_days = pd.DataFrame({
            "day": future_dates.dayofyear
        })

        # 🔹 Predict
        preds = model.predict(future_days)

        # 🔥 Convert to DataFrame (VERY IMPORTANT)
        result_df = pd.DataFrame({
            "date": future_dates,
            "predicted_revenue": preds
        })

        return result_df

    except Exception as e:
        return f"Forecast Error: {str(e)}"
