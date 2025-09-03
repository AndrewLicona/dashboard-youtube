import streamlit as st
import pandas as pd
import plotly.express as px


# ======================
# 0️⃣ Cargar datos desde CSV (cacheado para rendimiento)
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data/daily_stats.csv", parse_dates=["day"])
    df["day"] = df["day"].dt.normalize()  # ✅ Normalizar solo una vez
    return df

df = load_data()

# ======================
# 🔄 Filtrar datos por rango (cacheado)
# ======================
@st.cache_data
def filter_data(df, dias):
    if dias is None:  # Todo el historial
        return df.copy(), df["day"].min(), df["day"].max()
    fin = df["day"].max()
    ini = fin - pd.Timedelta(days=dias - 1)
    df_sel = df[(df["day"] >= ini) & (df["day"] <= fin)].copy()
    return df_sel, ini, fin

# ======================
# 1️⃣ Función principal
# ======================
def show_daily_stats(df):
    st.title("📊 Estadísticas de YouTube (Daily Stats)")

    # ======================
    # 2️⃣ Selector de rango (últimos X días)
    # ======================
    opciones = {
        "Últimos 7 días": 7,
        "Últimos 28 días": 28,
        "Últimos 60 días": 60,
        "Últimos 90 días": 90,
        "Último año": 365,
        "Todo": None
    }

    periodo = st.selectbox("Selecciona el rango de tiempo:", list(opciones.keys()))
    df_sel, ini, fin = filter_data(df, opciones[periodo])

    if df_sel.empty:
        st.warning("⚠️ No hay datos en el rango seleccionado.")
        return

    # ======================
    # 3️⃣ Gráficos individuales (pestañas)
    # ======================
    st.subheader(f"📊 Evolución diaria ({ini.strftime('%d-%b-%Y')} a {fin.strftime('%d-%b-%Y')})")
    tabs = st.tabs(["📌 Vistas", "👍 Likes", "💬 Comentarios"])
    metrics = ["views", "likes", "comments"]

    for i, metric in enumerate(metrics):
        with tabs[i]:
            etiquetas = df_sel["day"].dt.strftime("%d-%b-%Y")
            fig = px.bar(
                df_sel,
                x=etiquetas,
                y=metric,
                labels={"x": "Fecha", metric: metric.capitalize()},
                title=f"{metric.capitalize()} diarios"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ======================
    # 4️⃣ Gráfico acumulado (curvas)
    # ======================
    df_sel["views_cumsum"] = df_sel["views"].cumsum()
    df_sel["likes_cumsum"] = df_sel["likes"].cumsum()
    df_sel["comments_cumsum"] = df_sel["comments"].cumsum()

    fig_line = px.line(
        df_sel,
        x="day",
        y=["views_cumsum", "likes_cumsum", "comments_cumsum"],
        markers=True,
        title="📈 Evolución acumulada (Vistas, Likes, Comentarios)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ======================
    # 5️⃣ Métricas rápidas
    # ======================
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Vistas", f"{int(df_sel['views'].sum()):,}")
    col2.metric("👍 Total Likes", f"{int(df_sel['likes'].sum()):,}")
    col3.metric("💬 Total Comentarios", f"{int(df_sel['comments'].sum()):,}")

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Promedio Vistas/día", f"{int(df_sel['views'].mean()):,}")
    col2.metric("👍 Promedio Likes/día", f"{int(df_sel['likes'].mean()):,}")
    col3.metric("💬 Promedio Comentarios/día", f"{int(df_sel['comments'].mean()):,}")

    max_dia = df_sel.loc[df_sel["views"].idxmax()]
    st.info(f"📌 Mejor día de vistas: {max_dia['day'].strftime('%d-%b-%Y')} con {max_dia['views']:,} vistas")
