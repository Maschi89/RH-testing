import streamlit as st
import pandas as pd
import random
import time

# 1. TA CONFIGURATION (URL mise à jour)
# Remplace la partie entre guillemets si tu changes de document plus tard
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6zSndh461zL_27pI61l9mUfWp0U_V2E_p2Y9_rY4_n1_n1_n1/pub?output=csv" 

st.set_page_config(page_title="IA Advisor Prototype", layout="centered")

# --- INTERFACE ---
st.title("🤖 Assistant Intelligent Pro")
st.write("Utilisez notre base de données et demandez un conseil à l'IA pour optimiser vos choix.")

try:
    # Chargement des données
    # On ajoute un paramètre de mise en cache pour éviter de recharger le CSV à chaque clic
    @st.cache_data(ttl=300) # Rafraîchit les données toutes les 5 minutes
    def load_data(url):
        return pd.read_csv(url)

    df = load_data(SHEET_URL)

    # BARRE DE RECHERCHE
    query = st.text_input("Que recherchez-vous aujourd'hui ?", placeholder="Ex: Marketing, Finance, Outils...")

    if query:
        # Filtrage simple
        results = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
        
        if not results.empty:
            st.success(f"Nous avons trouvé {len(results)} correspondances.")
            st.dataframe(results, use_container_width=True)

            st.divider()

            # --- LE BOUTON "CONSEIL DE L'IA" (Ton Test de Valeur) ---
            st.subheader("Besoin d'aller plus loin ?")
            if st.button("✨ Obtenir un Conseil de l'IA"):
                # Simulation de réflexion de l'IA
                with st.spinner('L\'IA analyse vos données...'):
                    time.sleep(2) # Donne un aspect "réel" au calcul
                    
                    # Liste de conseils pour le prototype
                    conseil_aleatoire = [
                        "D'après les tendances, vous devriez vous concentrer sur la colonne 2 ce mois-ci.",
                        "L'analyse prédictive suggère que cet élément est le plus rentable pour votre profil.",
                        "Optimisez votre recherche en ajoutant un critère de budget pour un meilleur résultat.",
                        "Attention : les données indiquent une saturation sur ce secteur, diversifiez vos sources."
                    ]
                    st.info(f"**Conseil de l'IA :** {random.choice(conseil_aleatoire)}")
                    
                # Message discret pour le testeur
                st.caption("ℹ️ Feedback enregistré pour améliorer l'algorithme.")

        else:
            st.warning("Aucun résultat pour cette recherche.")

except Exception as e:
    st.error("Erreur de connexion aux données.")
    st.info("Vérifiez que le Google Sheet est bien 'Publié sur le Web' au format CSV.")
    # Affiche l'erreur précise pour le debug au besoin
    # st.write(e)

# --- FOOTER DISCRET ---
st.markdown("---")
st.caption("Prototype v1.3 - Testing Mode Active")
