
import streamlit as st
import difflib

# --- Données enrichies pour le prototype ---
belief_data = [
    {
        "statement": "La Terre est plate",
        "countries": [
            {"name": "États-Unis", "percentage": 2, "source": "YouGov 2018", "continent": "Amérique du Nord"},
            {"name": "Brésil", "percentage": 7, "source": "Datafolha 2021", "continent": "Amérique du Sud"},
            {"name": "Turquie", "percentage": 10, "source": "Gezici 2020", "continent": "Asie"}
        ],
        "global_estimate": 5,
        "scientific_consensus": "Faux",
        "notes": "Consensus scientifique basé sur l'astronomie moderne et les données satellites."
    },
    {
        "statement": "Les vaccins causent l'autisme",
        "countries": [
            {"name": "États-Unis", "percentage": 10, "source": "Pew 2019", "continent": "Amérique du Nord"},
            {"name": "France", "percentage": 18, "source": "Ifop 2020", "continent": "Europe"}
        ],
        "global_estimate": 12,
        "scientific_consensus": "Faux",
        "notes": "Aucune preuve scientifique ne soutient cette affirmation (CDC, OMS)."
    },
    {
        "statement": "L'astrologie influence la personnalité",
        "countries": [
            {"name": "Royaume-Uni", "percentage": 33, "source": "YouGov 2022", "continent": "Europe"},
            {"name": "Inde", "percentage": 62, "source": "India Today 2021", "continent": "Asie"}
        ],
        "global_estimate": 40,
        "scientific_consensus": "Faux",
        "notes": "Aucune preuve scientifique, mais croyance culturelle très répandue."
    },
    {
        "statement": "Le changement climatique est causé par l'homme",
        "countries": [
            {"name": "Allemagne", "percentage": 83, "source": "Eurobaromètre 2021", "continent": "Europe"},
            {"name": "États-Unis", "percentage": 59, "source": "Pew 2020", "continent": "Amérique du Nord"}
        ],
        "global_estimate": 70,
        "scientific_consensus": "Vrai",
        "notes": "Consensus scientifique établi (GIEC, IPCC)."
    }
]

# --- Fonction de recherche floue ---
def search_belief_local(statement: str) -> dict:
    statements = [b["statement"] for b in belief_data]
    match = difflib.get_close_matches(statement, statements, n=1, cutoff=0.4)
    if match:
        for belief in belief_data:
            if belief["statement"] == match[0]:
                return belief
    return {
        "statement": statement,
        "countries": [],
        "global_estimate": 0.0,
        "scientific_consensus": "Inconnu",
        "notes": "Aucune donnée disponible sur cette affirmation."
    }

# --- Interface Streamlit ---
st.set_page_config(page_title="Moteur de Croyances", layout="centered")
st.title("Moteur de recherche d'opinions populaires")

user_input = st.text_input("Tape une affirmation (ex: 'Les vaccins causent l'autisme'):")
continent_filter = st.selectbox("Filtrer par continent (optionnel) :", ["Tous", "Europe", "Amérique du Nord", "Amérique du Sud", "Asie", "Afrique"])

if user_input:
    result = search_belief_local(user_input)

    st.subheader(f"Résultats pour : {result['statement']}")
    if result["countries"]:
        st.write(f"**Consensus scientifique** : {result['scientific_consensus']}")
        st.write(f"**Estimation globale** : {result['global_estimate']}%")
        st.markdown("---")

        for country in result["countries"]:
            if continent_filter == "Tous" or country.get("continent") == continent_filter:
                st.write(f"**{country['name']}** ({country['continent']}) : {country['percentage']}% ({country['source']})")

        st.markdown("---")
        st.write(f"**Note** : {result['notes']}")
    else:
        st.warning("Aucune donnée disponible sur cette affirmation.")
