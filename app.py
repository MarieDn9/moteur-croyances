import streamlit as st
import difflib
import pandas as pd
import plotly.express as px
import json
from collections import Counter

# --- Chargement des données ---
with open("beliefs.json", "r", encoding="utf-8") as f:
    belief_data = json.load(f)

# --- Recherche floue ---
def search_belief_local(statement: str) -> dict:
    statements = [b["statement"] for b in belief_data]
    match = difflib.get_close_matches(statement, statements, n=1, cutoff=0.4)
    if match:
        for belief in belief_data:
            if belief["statement"] == match[0]:
                return belief

    keywords = statement.lower().split()
    for belief in belief_data:
        for word in keywords:
            if word in belief["statement"].lower():
                return belief

    return {
        "statement": statement,
        "countries": [],
        "global_estimate": 0.0,
        "scientific_consensus": "Inconnu",
        "notes": "Aucune donnée disponible sur cette affirmation ou mot-clé.",
        "metadata": {},
        "demographics": {},
        "year": None,
        "theme": ""
    }

# --- Design personnalisé ---
st.set_page_config(page_title="Moteur de Croyances", layout="centered")
st.markdown("""
    <style>
    html, body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen;
        background-color: #f4f6f8;
        color: #222;
    }
    .stat-box {
        background-color: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .highlight-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1e90ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🔍 Moteur de recherche d'opinions</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Interrogez les croyances populaires par pays et par période.</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation", ["🔍 Moteur de recherche", "📈 Statistiques générales"])

if menu == "📈 Statistiques générales":
    st.subheader("📊 Statistiques globales sur les croyances")

    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='highlight-title'>📌 Nombre total de croyances : {len(belief_data)}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    themes = [b.get("theme", "Non classé") for b in belief_data if b.get("theme")]
    theme_count = Counter(themes)
    theme_df = pd.DataFrame(theme_count.items(), columns=["Thème", "Nombre de croyances"])

    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.markdown("<div class='highlight-title'>🧩 Répartition par thème</div>", unsafe_allow_html=True)
    fig_theme = px.bar(theme_df.sort_values("Nombre de croyances", ascending=False), x="Thème", y="Nombre de croyances",
                       color="Nombre de croyances", color_continuous_scale="Blues")
    st.plotly_chart(fig_theme, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    top_global = sorted(belief_data, key=lambda b: b.get("global_estimate", 0), reverse=True)[:10]
    top_df = pd.DataFrame([{"Croyance": b["statement"], "% d'accord (monde)": b["global_estimate"]} for b in top_global])

    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.markdown("<div class='highlight-title'>🌍 Top 10 des croyances les plus partagées globalement</div>", unsafe_allow_html=True)
    fig_top = px.bar(top_df, x="% d'accord (monde)", y="Croyance", orientation="h", color="% d'accord (monde)",
                     color_continuous_scale="Bluered", height=500)
    fig_top.update_layout(yaxis_title="", xaxis_title="% d'accord")
    st.plotly_chart(fig_top, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔍 Moteur de recherche":
    st.subheader("🔎 Recherchez une croyance")

    query = st.text_input("Entrez une croyance ou un mot-clé (ex : 'L’homme n’a jamais marché sur la lune')")

    if query:
        result = search_belief_local(query)

        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='highlight-title'>{result['statement']}</div>", unsafe_allow_html=True)

        if result["year"]:
            st.write(f"📅 Année : {result['year']}")
        if result["theme"]:
            st.write(f"🏷️ Thème : {result['theme']}")
        if result["global_estimate"]:
            st.write(f"🌍 Estimation globale : {result['global_estimate']}%")
        if result["scientific_consensus"] and result["scientific_consensus"] != "Inconnu":
            st.write(f"📚 Consensus scientifique : {result['scientific_consensus']}")
        if result["countries"]:
            st.write("📊 Estimations par pays :")
            st.write(result["countries"])
        if result["demographics"]:
            st.write("👥 Démographie :")
            st.write(result["demographics"])
        if result["notes"]:
            st.markdown(f"📝 _{result['notes']}_")

        st.markdown("</div>", unsafe_allow_html=True)
