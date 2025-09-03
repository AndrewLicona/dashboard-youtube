import streamlit as st
from section.dashboard import show
from section.estadisticas import show_time_comparisons
from section.data_stats import show_daily_stats
from fetchs.fetch_data import fetch_all_videos
from fetchs.fetch_daily import fetch_daily_stats
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = os.getenv("CHANNEL_ID")
API_KEY = os.getenv("API_KEY")

# ======================
# Cachear las llamadas a la API
# ======================
@st.cache_data
def get_all_videos(channel_id):
    return fetch_all_videos(channel_id)

@st.cache_data
def get_daily_stats(channel_id):
    return fetch_daily_stats(channel_id)

# ======================
# Cargar datasets SOLO una vez
# ======================
df = get_all_videos(CHANNEL_ID)
df_daily = get_daily_stats(CHANNEL_ID)

# ======================
# Layout principal con pestañas
# ======================
st.title("📊 Estadísticas de YouTube")
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard - AJDREW Gameplays",
    "▶️ Estadísticas por fecha",
    "📈 Comparativa de videos"
])

with tab1:
    show(df)

with tab2:
    show_time_comparisons(df)

with tab3:
    show_daily_stats(df_daily)
