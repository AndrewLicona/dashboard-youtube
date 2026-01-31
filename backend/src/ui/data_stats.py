import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.core.config import DATA_DIR, logger

def filter_data(df, dias):
    """Filtra el dataframe por el número de días especificado."""
    if dias is None or df.empty:
        return df.copy(), (df["day"].min() if not df.empty else None), (df["day"].max() if not df.empty else None)
    
    fin = df["day"].max()
    ini = fin - pd.Timedelta(days=dias - 1)
    df_sel = df[(df["day"] >= ini) & (df["day"] <= fin)].copy()
    return df_sel, ini, fin

def show_daily_stats(df):
    """Muestra estadísticas diarias detalladas."""
    
    # 1. Filtros de Tiempo
    st.markdown("### ⏲️ Análisis Histórico Detallado")
    
    opciones = {
        "Última Semana": 7,
        "Último Mes": 28,
        "Último Trimestre": 90,
        "Año Completo": 365,
        "Historial Total": None
    }
    
    col_sel, col_info = st.columns([1, 2])
    with col_sel:
        periodo = st.selectbox("Rango de consulta:", list(opciones.keys()))
        df_sel, ini, fin = filter_data(df, opciones[periodo])

    if df_sel.empty:
        st.warning("No hay registros para el periodo seleccionado.")
        return

    # 2. Resumen Numérico
    with st.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Vistas Totales", f"{int(df_sel['views'].sum()):,}")
        c2.metric("Media de Vistas/Día", f"{int(df_sel['views'].mean()):,}")
        max_dia = df_sel.loc[df_sel["views"].idxmax()]
        c3.metric("Pico de Audiencia", f"{int(max_dia['views']):,}", f"en {max_dia['day'].strftime('%d %b')}")

    st.divider()

    # 3. Gráficos de Evolución
    st.markdown(f"### 📈 Evolución Diaria ({ini.strftime('%d/%m/%y')} - {fin.strftime('%d/%m/%y')})")
    
    metric_choice = st.segmented_control("Seleccionar Métrica Principal:", 
                                       ["views", "likes", "comments"], 
                                       default="views",
                                       format_func=lambda x: x.capitalize())

    fig_daily = px.area(df_sel, x="day", y=metric_choice, 
                       title=f"Tendencia de {metric_choice.capitalize()}",
                       color_discrete_sequence=["#FF0000"])
    
    fig_daily.update_layout(
        template="plotly_white",
        xaxis_title="Día",
        yaxis_title="Cantidad",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # 4. Acumulados
    with st.expander("Ver crecimiento acumulado"):
        df_sel["views_cum"] = df_sel["views"].cumsum()
        fig_cum = px.line(df_sel, x="day", y="views_cum", title="Crecimiento Acumulado de Vistas")
        st.plotly_chart(fig_cum, use_container_width=True)
