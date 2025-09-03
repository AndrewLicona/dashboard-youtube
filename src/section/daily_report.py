import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from src.fetchs.fetch_daily import fetch_daily_stats

load_dotenv()

if __name__ == "__main__":
    channel_id = os.getenv("CHANNEL_ID")

    # 1️⃣ Descargar datos últimos 30 días
    df_daily = fetch_daily_stats(channel_id, days=30, metrics="views")

    # 2️⃣ Guardar CSV
    os.makedirs("data", exist_ok=True)
    df_daily.to_csv("data/daily_stats.csv", index=False, encoding="utf-8-sig")
    print("✅ Datos diarios guardados en data/daily_stats.csv")

    # 3️⃣ Graficar
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))

    # Últimos 7 días
    df_last7 = df_daily.tail(7)
    ax[0].bar(df_last7["day"].dt.strftime("%Y-%m-%d"), df_last7["views"])
    ax[0].set_title("📊 Vistas en los últimos 7 días")
    ax[0].set_ylabel("Vistas")

    # Últimos 30 días
    ax[1].bar(df_daily["day"].dt.strftime("%Y-%m-%d"), df_daily["views"])
    ax[1].set_title("📊 Vistas en los últimos 30 días")
    ax[1].set_ylabel("Vistas")
    ax[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()
