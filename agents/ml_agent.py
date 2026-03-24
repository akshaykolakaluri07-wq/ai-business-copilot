import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast(df):
    if isinstance(df, str):
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.dayofyear

    X = df[["day"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = pd.DataFrame({"day": range(366, 371)})
    preds = model.predict(future_days)

    return preds.tolist()
