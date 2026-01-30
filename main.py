import streamlit as st
import os
from src.ui.dashboard import show
from src.ui.estadisticas import show_time_comparisons
from src.ui.data_stats import show_daily_stats
from src.services.fetch_data import fetch_all_videos
from src.services.fetch_daily import fetch_daily_stats
from src.core.config import CHANNEL_ID, logger

# ======================
# Configuración de Página
# ======================
st.set_page_config(
    page_title="AJDREW Analytics | Dashboard",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# COLOR PALETTE: Gamer Green (Green: #00C851, Dark: #0F0F0F, Card: #1A1A1A, Silver: #CCCCCC)
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
    /* 1. Fondo Principal */
    .stApp {
        background-color: #0F0F0F !important;
        color: #FFFFFF !important;
    }

    /* 2. Tarjetas de Métricas (KPIs) - ALTA VISIBILIDAD */
    div[data-testid="stMetric"] {
        background-color: #1A1A1A !important;
        border: 2px solid #222222 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }

    /* Label de la métrica */
    div[data-testid="stMetricLabel"] > div {
        color: #AAAAAA !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }

    /* Valor de la métrica */
    div[data-testid="stMetricValue"] > div {
        color: #00C851 !important; /* Verde Gamer */
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }

    /* 3. Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1A1A1A !important;
        border-radius: 8px 8px 0 0 !important;
        color: #AAAAAA !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border: 1px solid #333333 !important;
        border-bottom: none !important;
    }

    /* Tab Activo */
    .stTabs [aria-selected="true"] {
        background-color: #00C851 !important; /* Verde Gamer */
        color: #000000 !important; /* Texto negro para contraste en verde */
        border: 1px solid #00C851 !important;
        box-shadow: 0 -4px 10px rgba(0, 200, 81, 0.3) !important;
    }

    /* 4. Cabecera Responsiva */
    @media (max-width: 640px) {
        .m-icon { font-size: 1.5rem !important; }
        h1 { font-size: 1.8rem !important; }
        div[data-testid="column"] { width: 100% !important; margin-bottom: 20px; }
    }

    .channel-badge {
        background-color: #00C851;
        color: black;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        vertical-align: middle;
    }

    .m-icon {
        vertical-align: middle;
        margin-right: 12px;
        font-size: 2rem;
        color: #00C851;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# Datos y Caché
# ======================
@st.cache_data
def get_all_videos(channel_id):
    return fetch_all_videos(channel_id)

@st.cache_data
def get_daily_stats(channel_id):
    return fetch_daily_stats(channel_id)

# Carga
with st.spinner("🚀 Cargando Suite Gamer..."):
    df = get_all_videos(CHANNEL_ID)
    df_daily = get_daily_stats(CHANNEL_ID)

# ======================
# Cabecera
# ======================
col_title, col_user = st.columns([5, 1])
with col_title:
    st.markdown("# <i class='material-icons m-icon'>query_stats</i> AJDREW Analytics", unsafe_allow_html=True)
    st.markdown(f"Canal: **AJDREW Gameplays** <span class='channel-badge'>LIVE</span>", unsafe_allow_html=True)

with col_user:
    st.markdown("<div style='text-align: right;'><i class='material-icons' style='font-size: 45px; color: #333333;'>account_circle</i></div>", unsafe_allow_html=True)

st.divider()

# ======================
# Navegación
# ======================
if df.empty:
    st.error("⚠️ Datos no disponibles.")
else:
    tab1, tab2, tab3 = st.tabs(["📊 DASHBOARD", "🕒 TIEMPO", "📈 DAILY"])

    with tab1:
        show(df)

    with tab2:
        show_time_comparisons(df)

    with tab3:
        if df_daily.empty:
            st.warning("⚠️ Sin datos de Analytics (403).")
        else:
            show_daily_stats(df_daily)
