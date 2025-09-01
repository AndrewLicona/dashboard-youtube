import streamlit as st
from pages.dashboard import show
from pages.estadisticas import show_time_comparisons
from fetch_data import fetch_all_videos
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = os.getenv("CHANNEL_ID")
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Dashboard YouTube", layout="wide")

# Ocultar el main y redirigir al dashboard
df = fetch_all_videos(CHANNEL_ID)
show()
show_time_comparisons(df)
