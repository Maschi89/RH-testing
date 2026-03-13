import streamlit as st
import pandas as pd
import random
import time

# --- CONFIGURATION ---
# REMPLACE BIEN TOUTE L'URL CI-DESSOUS PAR LA TIENNE
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6zSndh461zL_27pI61l9mUfWp0U_V2E_p2Y9_rY4_n1_n1_n1/pub?output=csv"

st.set_page_config(page_title="IA Advisor Prototype", layout="centered")

st.title("🤖 Assistant Intelligent Pro")
st.write("Utilisez notre base de données et demandez un conseil à l'IA.")

try:
    @st.cache_data(ttl=300)
    def load_data(url):
        # On nettoie l'URL au cas où un espace se serait glissé
        return pd.read_csv(url.strip())

    df = load_data(SHEET_URL)

    query = st.text_input("Que recherchez-vous ?", placeholder="Ex: Marketing...")

    if query:
        results = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
        
        if not results.empty:
            st.success(f"Trouvé : {len(results)} résultats.")
            st.dataframe(results, use_container_width=True)
            st.divider()
            if st.button("✨ Obtenir un Conseil de l'IA"):
                with st.spinner('Analyse...'):
                    time.sleep(1.5)
                    conseils = [
                        "Optimisez la colonne 2 ce mois-ci.",
                        "Élément très rentable détecté.",
                        "Diversifiez vos sources selon l'analyse."
                    ]
                    st.info(f"**Conseil :** {random.choice(conseils)}")
        else:
            st.warning("Aucun résultat.")

except Exception as e:
    st.error("Erreur de connexion aux données.")
    st.exception(e) # Version plus complète pour voir l'erreur sur Streamlit
