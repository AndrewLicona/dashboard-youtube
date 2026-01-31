from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    
    # Encrypted tokens using Fernet
    access_token_enc = Column(String, nullable=True)
    refresh_token_enc = Column(String, nullable=True)
    
    email = Column(String, nullable=True)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    metrics = relationship("DailyMetric", back_populates="channel", cascade="all, delete-orphan")

class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    channel_id_fk = Column(Integer, ForeignKey("channels.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    views = Column(BigInteger, default=0)
    likes = Column(BigInteger, default=0)
    comments = Column(BigInteger, default=0)
    subscribers = Column(BigInteger, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    channel = relationship("Channel", back_populates="metrics")
