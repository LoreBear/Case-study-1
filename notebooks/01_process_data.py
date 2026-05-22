# 01_process_data.py
import os
import glob
import pandas as pd

RAW_DIR = "data/raw"
OUT_DIR = "data/processed"
OUT_FILE = f"{OUT_DIR}/cyclistic_clean.csv"

os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{RAW_DIR}/*.csv"))
if len(files) == 0:
    raise SystemExit("Nessun CSV in data/raw. Scarica i file e riprova.")

frames = []
for f in files:
    df = pd.read_csv(f, low_memory=False)
    # normalizza nomi colonne
    df.columns = [c.strip().lower() for c in df.columns]
    # trova colonne data/ora start/end
    if "started_at" in df.columns and "ended_at" in df.columns:
        s_col, e_col = "started_at", "ended_at"
    elif "start_time" in df.columns and "end_time" in df.columns:
        s_col, e_col = "start_time", "end_time"
    else:
        # fallback: cerca colonne contenenti 'start' e 'end'
        s_candidates = [c for c in df.columns if "start" in c]
        e_candidates = [c for c in df.columns if "end" in c]
        if not s_candidates or not e_candidates:
            raise SystemExit(f"Colonne data/ora non trovate in {f}")
        s_col, e_col = s_candidates[0], e_candidates[0]

    # rinomina in modo coerente
    df = df.rename(columns={s_col: "started_at", e_col: "ended_at"})

    # parsing date
    df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
    df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")

    # rimuovi righe senza timestamp validi
    df = df.dropna(subset=["started_at", "ended_at"])

    # calcolo durata in secondi e minuti
    df["ride_length_seconds"] = (df["ended_at"] - df["started_at"]).dt.total_seconds()
    df["ride_length_minutes"] = df["ride_length_seconds"] / 60.0

    # normalizza colonna tipo utente
    for candidate in ["member_casual", "user_type", "usertype", "membertype"]:
        if candidate in df.columns:
            df = df.rename(columns={candidate: "member_casual"})
            break

    frames.append(df)

# unisci tutto
full = pd.concat(frames, ignore_index=True)

# filtri logici: durata positiva e <= 24 ore (86400 s)
full = full[(full["ride_length_seconds"] > 0) & (full["ride_length_seconds"] <= 86400)]

# aggiungi giorno della settimana e mese/anno
full["day_of_week"] = full["started_at"].dt.day_name()
full["month"] = full["started_at"].dt.to_period("M").astype(str)
full["hour_of_day"] = full["started_at"].dt.hour

# salva file pulito
full.to_csv(OUT_FILE, index=False)
print("Salvato:", OUT_FILE)
print("Righe totali:", len(full))
