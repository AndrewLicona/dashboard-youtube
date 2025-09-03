import pandas as pd
from datetime import date
import os
from dotenv import load_dotenv
from src.api_youtube_analytics import get_youtube_analytics_service

load_dotenv()

def fetch_daily_stats(channel_id, start_date=None, end_date=None, metrics="views,likes,comments"):
    youtube_analytics = get_youtube_analytics_service()

    # Fechas: desde el inicio del canal si no se pasa rango
    if end_date is None:
        end_date = (date.today() - pd.Timedelta(days=1)).isoformat()
    if start_date is None:
        start_date = "2022-12-31"  

    request = youtube_analytics.reports().query(
        ids=f"channel=={channel_id}",
        startDate=start_date,
        endDate=end_date,
        metrics=metrics,
        dimensions="day",
        sort="day"
    )
    response = request.execute()

    headers = [h["name"] for h in response["columnHeaders"]]
    rows = response.get("rows", [])

    df = pd.DataFrame(rows, columns=headers)
    df["day"] = pd.to_datetime(df["day"])
    return df

if __name__ == "__main__":
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        raise ValueError("❌ Define CHANNEL_ID en tu .env")

    # 🔥 Descargar toda la historia del canal
    df_daily = fetch_daily_stats(channel_id)

    # Guardar CSV
    os.makedirs("data", exist_ok=True)
    df_daily.to_csv("data/daily_stats.csv", index=False, encoding="utf-8-sig")
    print("✅ Datos diarios guardados en data/daily_stats.csv")
    print(df_daily.head())