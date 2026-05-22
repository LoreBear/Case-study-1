import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/cyclistic_clean.csv")
agg = df.groupby("member_casual")["ride_length_minutes"].agg(["mean","median","count"]).reset_index()
print(agg)

sns.barplot(x="member_casual", y="mean", data=agg.rename(columns={"mean":"mean"}))
plt.title("Durata media (min) - membri vs casual")
plt.savefig("reports/visuals/duration_mean_by_user.png", bbox_inches="tight")
plt.close()
by_day = df.groupby(["member_casual","day_of_week"])["ride_id" if "ride_id" in df.columns else df.columns[0]].count().reset_index()
# se no ride_id usa il conteggio su started_at
by_day.to_csv("reports/visuals/rides_by_day.csv", index=False)
# grafico heatmap esempio
table = df.pivot_table(index="day_of_week", columns="member_casual", values="ride_length_minutes", aggfunc="count").reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
sns.heatmap(table.fillna(0), annot=True, fmt=".0f")
plt.title("Numero corse per giorno x tipo utente")
plt.savefig("reports/visuals/rides_heatmap.png", bbox_inches="tight")
plt.close()
monthly = df.groupby(["month","member_casual"])["ride_length_minutes"].count().reset_index()
monthly_pivot = monthly.pivot(index="month", columns="member_casual", values="ride_length_minutes").fillna(0)
monthly_pivot.plot(kind="line")
plt.title("Numero corse per mese - membri vs casual")
plt.savefig("reports/visuals/rides_per_month.png", bbox_inches="tight")
plt.close()
