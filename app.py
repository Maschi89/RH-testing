import streamlit as st
import pandas as pd
import random
import time

# 1. TA CONFIGURATION
SHEET_URL = "TON_URL_PUBLIEE_ICI" # Remplace bien par ton lien se terminant par output=csv

st.set_page_config(page_title="IA Advisor Prototype", layout="centered")

# --- INTERFACE ---
st.title("🤖 Assistant Intelligent Pro")
st.write("Utilisez notre base de données et demandez un conseil à l'IA pour optimiser vos choix.")

try:
    # Chargement des données
    df = pd.read_csv(SHEET_URL)

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
                    
                    # Ici on simule un conseil basé sur la première ligne trouvée
                    conseil_aleatoire = [
                        "D'après les tendances, vous devriez vous concentrer sur la colonne 2 ce mois-ci.",
                        "L'analyse prédictive suggère que cet élément est le plus rentable pour votre profil.",
                        "Optimisez votre recherche en ajoutant un critère de budget pour un meilleur résultat."
                    ]
                    st.info(f"**Conseil de l'IA :** {random.choice(conseil_aleatoire)}")
                    
                # NOTE : Ici, en version "Connectée", on enverrait l'info 
                # "L'utilisateur X a cliqué sur Conseil IA" vers ton Google Sheet.
                st.caption("ℹ️ Feedback enregistré pour améliorer l'algorithme.")

        else:
            st.warning("Aucun résultat pour cette recherche.")

except Exception as e:
    st.error("Lien Google Sheet manquant ou mal configuré.")
    st.info("Vérifiez que vous avez bien mis l'URL de 'Publier sur le web' au format CSV.")

# --- FOOTER DISCRET ---
st.markdown("---")
st.caption("Prototype v1.2 - Testing Mode Active")
