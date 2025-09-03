import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def show_time_comparisons(df):
    """Muestra comparaciones de rendimiento en diferentes ventanas de tiempo."""
    dfc = df.copy()
    dfc["Publicado"] = pd.to_datetime(dfc["Publicado"], errors="coerce").dt.tz_localize(None)
    hoy = pd.Timestamp.today().normalize()

    # === 7 días vs 7 anteriores ===
    ini_7  = hoy - timedelta(days=7)
    ini_14 = hoy - timedelta(days=14)

    ultimos_7 = dfc[(dfc["Publicado"] >= ini_7) & (dfc["Publicado"] < hoy)]
    previos_7 = dfc[(dfc["Publicado"] >= ini_14) & (dfc["Publicado"] < ini_7)]

    v_ult7 = int(ultimos_7["Vistas"].sum())
    v_prev7 = int(previos_7["Vistas"].sum())
    l_ult7 = int(ultimos_7["Likes"].sum())
    l_prev7 = int(previos_7["Likes"].sum())
    c_ult7 = int(ultimos_7["Comentarios"].sum())
    c_prev7 = int(previos_7["Comentarios"].sum())

    st.subheader("🗓️ Últimos 7 días vs 7 anteriores")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vistas (últimos 7)", f"{v_ult7:,}", delta=v_ult7 - v_prev7)
    c2.metric("Likes (últimos 7)", f"{l_ult7:,}", delta=l_ult7 - l_prev7)
    c3.metric("Comentarios (últimos 7)", f"{c_ult7:,}", delta=c_ult7 - c_prev7)
    c4.metric("Videos publicados (últimos 7)", f"{len(ultimos_7):,}", delta=len(ultimos_7) - len(previos_7))

    # -----------------------
    # ÚLTIMOS 28 DÍAS vs 28 ANTERIORES
    # -----------------------
    ini_28 = hoy - timedelta(days=28)
    ini_56 = hoy - timedelta(days=56)

    ultimos_28 = dfc[(dfc["Publicado"] >= ini_28) & (dfc["Publicado"] < hoy)]
    previos_28 = dfc[(dfc["Publicado"] >= ini_56) & (dfc["Publicado"] < ini_28)]

    v_28 = int(ultimos_28["Vistas"].sum())
    v_prev28 = int(previos_28["Vistas"].sum())
    l_28 = int(ultimos_28["Likes"].sum())
    l_prev28 = int(previos_28["Likes"].sum())
    c_28 = int(ultimos_28["Comentarios"].sum())
    c_prev28 = int(previos_28["Comentarios"].sum())

    st.subheader("📊 Últimos 28 días vs 28 anteriores")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Vistas (28 días)", f"{v_28:,}", delta=v_28 - v_prev28)
    d2.metric("Likes (28 días)", f"{l_28:,}", delta=l_28 - l_prev28)
    d3.metric("Comentarios (28 días)", f"{c_28:,}", delta=c_28 - c_prev28)
    d4.metric("Videos (28 días)", f"{len(ultimos_28):,}", delta=len(ultimos_28) - len(previos_28))

    # -----------------------
    # COMPARACIÓN MES COMPLETO vs ANTERIOR (meses cerrados)
    # -----------------------
    dfc["MesPeriod"] = dfc["Publicado"].dt.to_period("M")
    resumen_m = (dfc.groupby("MesPeriod")
                    .agg(Vistas=("Vistas","sum"),
                         Likes=("Likes","sum"),
                         Comentarios=("Comentarios","sum"),
                         Videos=("Publicado","size"))
                    .reset_index())
    resumen_m["Mes_dt"] = resumen_m["MesPeriod"].dt.to_timestamp()
    resumen_m = resumen_m.sort_values("Mes_dt")

    inicio_mes_actual = hoy.replace(day=1)
    cerrados = resumen_m[resumen_m["Mes_dt"] < inicio_mes_actual]

    def mes_nombre(dt):
        return dt.strftime("%B %Y")  

    st.subheader("📆 Comparación mensual (mes cerrado vs anterior)")
    if len(cerrados) >= 2:
        last = cerrados.iloc[-1]
        prev = cerrados.iloc[-2]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f"Vistas en {mes_nombre(last['Mes_dt'])}", f"{int(last['Vistas']):,}", delta=int(last['Vistas'] - prev['Vistas']))
        col2.metric(f"Likes en {mes_nombre(last['Mes_dt'])}", f"{int(last['Likes']):,}", delta=int(last['Likes'] - prev['Likes']))
        col3.metric(f"Comentarios en {mes_nombre(last['Mes_dt'])}", f"{int(last['Comentarios']):,}", delta=int(last['Comentarios'] - prev['Comentarios']))
        col4.metric(f"Videos en {mes_nombre(last['Mes_dt'])}", f"{int(last['Videos']):,}", delta=int(last['Videos'] - prev['Videos']))
    else:
        st.info("Aún no hay dos meses cerrados para comparar.")

    # -----------------------
    # TOP DE MESES por métricas (cerrados)
    # -----------------------
    if not cerrados.empty:
        cerrados["Mes_nombre"] = cerrados["Mes_dt"].dt.strftime("%B %Y")
        colA, colB = st.columns(2)

        with colA:
            top_v = cerrados.sort_values("Vistas", ascending=False).head(10)
            fig_mv = px.bar(top_v, x="Vistas", y="Mes_nombre", orientation="h", title="Top meses por Vistas")
            fig_mv.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_mv, use_container_width=True)

            top_l = cerrados.sort_values("Likes", ascending=False).head(10)
            fig_ml = px.bar(top_l, x="Likes", y="Mes_nombre", orientation="h", title="Top meses por Likes")
            fig_ml.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_ml, use_container_width=True)

        with colB:
            top_c = cerrados.sort_values("Comentarios", ascending=False).head(10)
            fig_mc = px.bar(top_c, x="Comentarios", y="Mes_nombre", orientation="h", title="Top meses por Comentarios")
            fig_mc.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_mc, use_container_width=True)

            top_vid = cerrados.sort_values("Videos", ascending=False).head(10)
            fig_mvid = px.bar(top_vid, x="Videos", y="Mes_nombre", orientation="h", title="Top meses por Videos publicados")
            fig_mvid.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_mvid, use_container_width=True)

    # -----------------------
    # RENDIMIENTO POR DÍA DE LA SEMANA
    # -----------------------
    st.subheader("📅 Rendimiento por día de la semana (promedio por video)")
    dfc["weekday_num"] = dfc["Publicado"].dt.weekday  # 0=Lunes
    dias = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
    dfc["Día"] = dfc["weekday_num"].map(dias)

    by_weekday = (dfc.groupby("Día")
                    .agg(Vistas_prom=("Vistas","mean"),
                         Likes_prom=("Likes","mean"),
                         Coment_prom=("Comentarios","mean"),
                         Videos=("Publicado","size"))
                    .reset_index())

    orden_sem = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    by_weekday["Día"] = pd.Categorical(by_weekday["Día"], categories=orden_sem, ordered=True)
    by_weekday = by_weekday.sort_values("Día")

    fig_wd = px.bar(by_weekday, x="Día", y="Vistas_prom", title="Vistas promedio por video según día de publicación")
    st.plotly_chart(fig_wd, use_container_width=True)

# === LLAMADA: pega esto donde ya tengas df cargado ===
#show_time_comparisons(df)


# def app():
#     st.title("📈 Estadísticas avanzadas")
#     df = fetch_all_videos(channel_id=os.getenv("CHANNEL_ID"))
#     show_time_comparisons(df)

# app()