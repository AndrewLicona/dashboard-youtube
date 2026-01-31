import os
import pandas as pd
from datetime import datetime, timedelta
from src.core.config import logger, DATA_DIR
from src.services.api_youtube_analytics import get_youtube_analytics_service

def fetch_daily_stats(channel_id, start_date=None, end_date=None, metrics="views,likes,comments,subscribersGained"):
    """Consulta reportes diarios de YouTube Analytics."""
    try:
        youtube_analytics = get_youtube_analytics_service(channel_id)
        if not youtube_analytics:
             logger.warning(f"No hay servicio de Analytics disponible para {channel_id} (Falta Token).")
             return pd.DataFrame()

        # Fechas: desde el inicio del canal si no se pasa rango
        if end_date is None:
            end_date = (date.today() - pd.Timedelta(days=1)).isoformat()
        if start_date is None:
            start_date = "2022-12-31"  

        logger.info(f"Consultando estadísticas diarias desde {start_date} hasta {end_date}...")

        request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics=metrics,
            dimensions="day",
            sort="day"
        )
        response = request.execute()

        headers = [h["name"] for h in response.get("columnHeaders", [])]
        rows = response.get("rows", [])

        if not rows:
            logger.warning("No se encontraron datos en el reporte de Analytics.")
            return pd.DataFrame()

        df = pd.DataFrame(rows, columns=headers)
        if "subscribersGained" in df.columns:
            df.rename(columns={"subscribersGained": "subscribers"}, inplace=True)
            
        df["day"] = pd.to_datetime(df["day"])
        logger.info(f"Estadísticas diarias obtenidas: {len(df)} días.")
        return df
    except Exception as e:
        logger.error(f"Error al obtener estadísticas diarias de Analytics: {e}")
        return pd.DataFrame()