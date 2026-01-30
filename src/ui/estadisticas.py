import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta

def show_time_comparisons(df):
    """Muestra comparaciones en verde gamer."""
    dfc = df.copy()
    dfc["Publicado"] = pd.to_datetime(dfc["Publicado"], errors="coerce").dt.tz_localize(None)
    hoy = pd.Timestamp.today().normalize()

    st.markdown("### 📊 Ventana Temporal")
    ventana = st.radio("", ["7D", "28D"], horizontal=True, label_visibility="collapsed")

    dias = 7 if ventana == "7D" else 28
    
    ini_actual = hoy - timedelta(days=dias)
    ini_previo = hoy - timedelta(days=dias * 2)

    actual_df = dfc[(dfc["Publicado"] >= ini_actual) & (dfc["Publicado"] < hoy)]
    previo_df = dfc[(dfc["Publicado"] >= ini_previo) & (dfc["Publicado"] < ini_actual)]

    v_act = int(actual_df["Vistas"].sum())
    v_pre = int(previo_df["Vistas"].sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Vistas", f"{v_act:,}", delta=v_act - v_pre)
    c2.metric("Likes", f"{int(actual_df['Likes'].sum()):,}")
    c3.metric("Videos", len(actual_df))

    st.divider()

    # Gráfico de barras
    dfc["MesPeriod"] = dfc["Publicado"].dt.to_period("M")
    resumen_m = dfc.groupby("MesPeriod")["Vistas"].sum().reset_index()
    resumen_m["Mes"] = resumen_m["MesPeriod"].dt.to_timestamp()
    
    fig = px.bar(resumen_m.tail(6), x="Mes", y="Vistas", 
                 title="Vistas por Mes", 
                 color_discrete_sequence=["#00C851"])
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig, use_container_width=True)