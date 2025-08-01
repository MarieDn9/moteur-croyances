import streamlit as st
import difflib
import pandas as pd
import plotly.express as px
import json

# --- Chargement des données ---
with open("beliefs.json", "r", encoding="utf-8") as f:
    belief_data = json.load(f)

# --- Recherche floue ---
def search_belief_local(statement: str) -> dict:
    # Recherche d'abord sur les affirmations exactes ou proches
    statements = [b["statement"] for b in belief_data]
    match = difflib.get_close_matches(statement, statements, n=1, cutoff=0.4)
    if match:
        for belief in belief_data:
            if belief["statement"] == match[0]:
                return belief

    # Recherche sur les mots-clés
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
        "metadata": {}
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
    .stTextInput > div > div > input {
        text-align: center;
        padding: 1em;
        font-size: 1.1rem;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #1e90ff;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.5em 1em;
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Interface principale ---
st.markdown("<h1 style='text-align:center;'>🔍 Moteur de recherche d'opinions</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Interrogez les croyances populaires par pays et par période.</p>", unsafe_allow_html=True)

# ... (suite du fichier non réincluse ici pour simplifier)

