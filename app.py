import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURATION ---
# Remplace bien par ton URL réelle finissant par output=csv
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6zSndh461zL_27pI61l9mUfWp0U_V2E_p2Y9_rY4_n1_n1_n1/pub?output=csv"

st.set_page_config(page_title="RH Prototype Monitor", layout="wide")

st.title("📊 Dashboard de Suivi - Prototype RH")
st.write("Ce tableau de bord affiche en temps réel les interactions des utilisateurs sur Replit.")

# --- 2. CHARGEMENT DES DONNÉES ---
try:
    # On force le rafraîchissement toutes les 30 secondes pour voir les tests arriver
    @st.cache_data(ttl=30)
    def load_data(url):
        data = pd.read_csv(url)
        # On s'assure que la colonne Temps_Passe est bien lue comme un nombre
        if 'Temps_Passe' in data.columns:
            data['Temps_Passe'] = pd.to_numeric(data['Temps_Passe'], errors='coerce')
        return data

    df = load_data(SHEET_URL)

    # --- 3. RÉSUMÉ DES TESTS (STATISTIQUES) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nombre de tests", len(df))
    
    with col2:
        if 'Temps_Passe' in df.columns:
            moyenne = round(df['Temps_Passe'].mean(), 1)
            st.metric("Temps moyen (sec)", f"{moyenne}s")
            
    with col3:
        if 'Action' in df.columns:
            top_action = df['Action'].mode()[0] if not df.empty else "N/A"
            st.metric("Action la plus fréquente", top_action)

    st.divider()

    # --- 4. RECHERCHE ET TABLEAU ---
    st.subheader("🔍 Détail des interactions")
    query = st.text_input("Filtrer par action ou utilisateur (ex: Clic_Bot, User_1...)", "")

    if query:
        # Cherche le mot-clé dans toutes les colonnes
        results = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
        st.dataframe(results, use_container_width=True)
    else:
        # Affiche tout par défaut, du plus récent au plus ancien
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

except Exception as e:
    st.error("⚠️ En attente de données ou erreur de connexion.")
    st.info("Dès que le premier test sera effectué sur Replit, les données apparaîtront ici.")
    # Pour le débug : st.write(e)

# --- FOOTER ---
st.markdown("---")
st.caption("Mode : Shadow Testing en cours")
