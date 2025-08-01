
import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("beliefs.csv")
    return df

df = load_data()

# Interface principale
st.title("🔍 Moteur de recherche d'opinions")
st.markdown("Interrogez les croyances populaires par pays, thème, date ou profil démographique.")

# Filtres
col1, col2, col3 = st.columns(3)
with col1:
    selected_country = st.selectbox("🌍 Pays", ["Tous"] + sorted(df["pays"].dropna().unique().tolist()))
with col2:
    selected_theme = st.selectbox("🏷️ Thème", ["Tous"] + sorted(df["theme"].dropna().unique().tolist()))
with col3:
    selected_period = st.selectbox("📅 Période", ["Toutes"] + sorted(df["annee"].dropna().astype(str).unique().tolist()))

# Application des filtres
filtered_df = df.copy()
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df["pays"] == selected_country]
if selected_theme != "Tous":
    filtered_df = filtered_df[filtered_df["theme"] == selected_theme]
if selected_period != "Toutes":
    filtered_df = filtered_df[filtered_df["annee"].astype(str) == selected_period]

# Affichage des croyances filtrées
st.markdown("### Résultats")
if filtered_df.empty:
    st.info("Aucun résultat trouvé.")
else:
    for _, row in filtered_df.iterrows():
        st.markdown(f"**• {row['affirmation']}**")
        st.markdown(f"› {row['taux_adhesion']}% d'accord — {row['pays']}, {row['annee']}")
        if pd.notnull(row.get("source")):
            st.markdown(f"[Source]({row['source']})")

# Statistiques
st.markdown("---")
st.markdown("### 📊 Statistiques générales")

theme_counts = df["theme"].value_counts()
fig = px.bar(theme_counts, x=theme_counts.index, y=theme_counts.values,
             labels={"x": "Thème", "y": "Nombre de croyances"},
             title="Répartition des croyances par thème")
st.plotly_chart(fig)
