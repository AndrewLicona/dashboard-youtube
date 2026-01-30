import streamlit as st
import pandas as pd
import plotly.express as px

def show(df):
    """Muestra la vista principal del dashboard."""
    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    # === KPIs ===
    st.markdown("### 📌 KPIs Gamer")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Videos", f"{len(df):,}")
    c2.metric("Vistas", f"{df['Vistas'].sum():,}")
    c3.metric("Likes", f"{df['Likes'].sum():,}")
    c4.metric("Comments", f"{df['Comentarios'].sum():,}")

    st.divider()

    # === GRÁFICOS ===
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("### 📈 Evolución Vistas")
        df_hist = df.copy()
        df_hist["Publicado"] = pd.to_datetime(df_hist["Publicado"]).dt.tz_localize(None)
        df_hist["Mes"] = df_hist["Publicado"].dt.to_period("M").dt.to_timestamp()
        
        evol_mensual = df_hist.groupby("Mes")["Vistas"].sum().reset_index()
        
        fig_line = px.area(evol_mensual, x="Mes", y="Vistas", 
                          color_discrete_sequence=["#00C851"]) # Gamer Green
        
        fig_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFFFFF",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#222222")
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_side:
        st.markdown("### 🏆 Top 5")
        top_5 = df.nlargest(5, "Vistas")
        
        for i, row in top_5.iterrows():
            with st.container():
                # En mobile, usaremos 1 columna para que las imágenes se vean mejor
                c_img, c_txt = st.columns([1, 2])
                with c_img:
                    st.image(row["Miniatura"], width=100)
                with c_txt:
                    # Título más pequeño para mobile
                    st.markdown(f"<p style='font-size:0.85rem; font-weight:700; margin-bottom:0;'>{row['Titulo'][:40]}...</p>", unsafe_allow_html=True)
                    st.caption(f"👁️ {int(row['Vistas']):,} vistas")
            st.markdown("<div style='margin-bottom:10px; border-bottom:1px solid #222;'></div>", unsafe_allow_html=True)

    # DataFrame Expandible
    with st.expander("🔍 Detalles Completos"):
        st.dataframe(df[["Titulo", "Vistas", "Likes", "Comentarios"]], 
                     use_container_width=True)
