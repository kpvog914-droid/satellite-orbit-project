import pandas as pd

def load_solar_data(filepath="solar.csv"):
    df = pd.read_csv(filepath, skiprows=1, header=None)
    df.columns = ["Date", "F107"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    df["F107"] = df["F107"].replace(-9999, pd.NA)
    df = df.dropna()
    df["F107"] = pd.to_numeric(df["F107"]) / 10
    return df["F107"]
