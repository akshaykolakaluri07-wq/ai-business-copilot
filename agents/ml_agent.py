import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast(df, n_days=5):
    if isinstance(df, str):
        return df

    # Convert date
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Feature engineering
    df["day"] = df["date"].dt.dayofyear

    X = df[["day"]]
    y = df["revenue"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Get last date
    last_date = df["date"].max()

    # Generate future dates
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=n_days)

    future_days = pd.DataFrame({
        "day": future_dates.dayofyear
    })

    # Predict
    preds = model.predict(future_days)

    # Return clean output (date + prediction)
    result = []
    for date, pred in zip(future_dates, preds):
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted_revenue": float(pred)
        })

    return result
