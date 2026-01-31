import time
import schedule
from datetime import date, timedelta
from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.db.models import Channel, DailyMetric
from src.services.fetch_daily import fetch_daily_stats
from src.services.auth_service import get_credentials_from_db
from src.core.config import logger

def sync_daily_metrics_for_all_channels():
    """Recorre todos los canales y descarga sus métricas de ayer."""
    db: Session = SessionLocal()
    try:
        channels = db.query(Channel).all()
        logger.info(f"🔄 Iniciando sincronización diaria para {len(channels)} canales...")
        
        for ch in channels:
            logger.info(f"Checking channel: {ch.title} ({ch.channel_id})")
            
            # TODO: Add logic to check if we already have data for yesterday to save API quota
            
            # Fetch data using existing service (which now uses DB auth under the hood)
            # We fetch last 3 days just to be safe and ensure data consistency
            today = date.today()
            start_date = (today - timedelta(days=3)).isoformat()
            end_date = (today - timedelta(days=1)).isoformat()
            
            try:
                df = fetch_daily_stats(ch.channel_id, start_date=start_date, end_date=end_date)
                
                if df.empty:
                    logger.warning(f"No daily data found for {ch.title}")
                    continue
                    
                # Upsert into DB
                for _, row in df.iterrows():
                    row_date = row['day'].date() # Assuming 'day' is datetime from fetch_daily_stats logic
                    
                    # Check existence
                    metric = db.query(DailyMetric).filter(
                        DailyMetric.channel_id_fk == ch.id, # Use internal ID FK
                        DailyMetric.date == row_date
                    ).first()
                    
                    if not metric:
                        metric = DailyMetric(
                            channel_id_fk=ch.id,
                            date=row_date
                        )
                        db.add(metric)
                    
                    # Update fields
                    metric.views = row['views']
                    metric.likes = row['likes']
                    metric.comments = row['comments']
                    metric.subscribers = row['subscribers']
                
                db.commit()
                logger.info(f"✅ Synced {len(df)} days for {ch.title}")
                
            except Exception as e:
                logger.error(f"❌ Error syncing {ch.title}: {e}")
                db.rollback()

    except Exception as e:
        logger.error(f"Critical Cron Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Run once immediately for check
    sync_daily_metrics_for_all_channels()
    
    # Schedule every 24h
    # schedule.every().day.at("02:00").do(sync_daily_metrics_for_all_channels)
    
    # Loop
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
