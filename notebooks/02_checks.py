import pandas as pd
df = pd.read_csv("data/processed/cyclistic_clean.csv", nrows=1000)
print(df.columns.tolist())
print("Tipi utente:", df["member_casual"].value_counts(dropna=False))
print("Durata media (min):", df["ride_length_minutes"].mean())
print("Righe:", len(pd.read_csv("data/processed/cyclistic_clean.csv")))
