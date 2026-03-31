import pandas as pd
from sklearn.linear_model import LinearRegression
def forecast(df, n_days=5):
    if isinstance(df, str):
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.dayofyear

    X = df[["day"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    last_day = df["day"].max()

    future_days = pd.DataFrame({
        "day": range(last_day + 1, last_day + n_days + 1)
    })

    preds = model.predict(future_days)

    return preds.tolist()
