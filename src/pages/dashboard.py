import streamlit as st
import pandas as pd
import plotly.express as px
#from pages import estadisticas
# ==============================
# 📂 Cargar datos
# ==============================
@st.cache_data
def load_data():
    return pd.read_csv("data/videos.csv", parse_dates=["Publicado"])

df = load_data()
def show():
    # ==============================
    # 🎨 Configuración inicial
    # ==============================
    st.set_page_config(page_title="Dashboard YouTube AJDREW", layout="wide")
    st.title("📊 Dashboard - AJDREW Gameplays")
    # ==============================
    # 📌 Resumen general
    # ==============================
    st.subheader("Resumen general del canal")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de videos", len(df))
    col2.metric("Total de vistas", f"{df['Vistas'].sum():,}")
    col3.metric("Total de likes", f"{df['Likes'].sum():,}")
    col4.metric("Total de comentarios", f"{df['Comentarios'].sum():,}")

    # ==============================
    # 📈 Gráfico de evolución
    # ==============================
    st.subheader("Evolución de vistas en el tiempo")

    df_sorted = df.sort_values("Publicado")
    df_sorted["Vistas acumuladas"] = df_sorted["Vistas"].cumsum()

    opcion = st.radio("📌 Tipo de gráfico", ["Vistas acumuladas", "Vistas individuales"])

    if opcion == "Vistas acumuladas":
        fig_line = px.line(df_sorted, x="Publicado", y="Vistas acumuladas", title="Vistas acumuladas en el tiempo")
    else:
        fig_line = px.line(df_sorted, x="Publicado", y="Vistas", title="Vistas por video publicado")

    st.plotly_chart(fig_line, use_container_width=True)


    # ==============================
    # 📅 Evolución mensual
    # ==============================
    st.subheader("📅 Evolución mensual")

    # Crear columna de mes
    df["Mes"] = df["Publicado"].dt.to_period("M")

    # Agrupar por mes
    resumen_mensual = df.groupby("Mes").agg({
        "Vistas": "sum",
        "Likes": "sum",
        "Comentarios": "sum"
    }).reset_index()

    # Convertir a datetime
    resumen_mensual["Mes"] = resumen_mensual["Mes"].dt.to_timestamp()

    # 📈 Gráfico de vistas mensuales
    fig_mes = px.line(
        resumen_mensual,
        x="Mes",
        y="Vistas",
        markers=True,
        title="Evolución de vistas por mes"
    )
    st.plotly_chart(fig_mes, use_container_width=True)

    # ==============================
    # 🔄 Comparación último mes vs anterior
    # ==============================
    if len(resumen_mensual) >= 2:
        ultimo_mes = resumen_mensual.iloc[-1]
        mes_anterior = resumen_mensual.iloc[-2]

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Vistas último mes",
            f"{ultimo_mes['Vistas']:,}",
            delta=int(ultimo_mes["Vistas"] - mes_anterior["Vistas"])
        )
        col2.metric(
            "Likes último mes",
            f"{ultimo_mes['Likes']:,}",
            delta=int(ultimo_mes["Likes"] - mes_anterior["Likes"])
        )
        col3.metric(
            "Comentarios último mes",
            f"{ultimo_mes['Comentarios']:,}",
            delta=int(ultimo_mes["Comentarios"] - mes_anterior["Comentarios"])
        )
    else:
        st.info("Aún no hay suficientes meses para comparación 📊")


    # ==============================
    # 🏆 Top 10 videos más vistos
    # ==============================
    st.subheader("Top 10 videos más vistos")

    top_videos = df.sort_values("Vistas", ascending=False).head(10)
    top_videos = top_videos.iloc[::-1]  # mayor arriba
    top_videos["Título corto"] = top_videos["Título"].apply(
        lambda x: x if len(x) <= 50 else x[:47] + "..."
    )

    fig_bar = px.bar(
        top_videos,
        x="Vistas",
        y="Título corto",
        orientation="h",
        text="Vistas",
        
    )

    fig_bar.update_layout(yaxis_title="Título (corto)", xaxis_title="Vistas")

    st.plotly_chart(fig_bar, use_container_width=True)

    # ==============================
    # 🖼️ Tabla interactiva
    # ==============================
    st.subheader("Tabla de videos")

    # 👉 Selección de orden
    orden = st.selectbox("Ordenar por:", ["Publicado", "Vistas", "Likes", "Comentarios"])
    asc = st.checkbox("Orden ascendente", value=False)

    df_sorted_table = df.sort_values(by=orden, ascending=asc)

    # 👉 Paginación
    page_size = 10
    total_pages = (len(df_sorted_table) // page_size) + 1
    page_number = st.number_input("Página", min_value=1, max_value=total_pages, step=1)

    start = (page_number - 1) * page_size
    end = start + page_size
    df_page = df_sorted_table.iloc[start:end]

    # 👉 Convertir miniaturas a HTML
    def make_clickable(row):
        return f'<img src="{row["Miniatura"]}" width="120">'

    df_page_display = df_page[["Miniatura", "Título", "Publicado", "Vistas", "Likes", "Comentarios"]].copy()
    df_page_display["Miniatura"] = df_page_display.apply(make_clickable, axis=1)

    st.write(
        df_page_display.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
show()