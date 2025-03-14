import streamlit as st
import requests

# API_URL = "http://127.0.0.1:8000/insert"
API_URL = "http://serveur:8000/insert"

# API_URL = "http://backend:8000/insert"


st.title("Page Utilisateur - Insertion des données")

nom = st.text_input("Nom")
email = st.text_input("Email")
age = st.number_input("Âge", min_value=1, max_value=120, step=1)

if st.button("Enregistrer"):
    if nom and email and age:
        data = {"nom": nom, "email": email, "age": age}
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            st.success("Données insérées avec succès !")
        else:
            st.error(f"Erreur: {response.json()['detail']}")
    else:
        st.warning("Veuillez remplir tous les champs.")
