import streamlit as st
import requests

# API_GET_URL = "http://127.0.0.1:8000/get_all"
# API_UPDATE_URL = "http://127.0.0.1:8000/update"

API_GET_URL = "http://serveur:8000/get_all"
API_UPDATE_URL = "http://serveur:8000/update"

# Vérification des identifiants
def check_credentials(username, password):
    return username == "admin" and password == "password123"

# Interface de connexion
st.title("Page Admin")

username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    if check_credentials(username, password):
        st.success("Connexion réussie !")
        
        # Afficher les données
        st.subheader("Données dans la base")
        response = requests.get(API_GET_URL)

        if response.status_code == 200:
            data = response.json()
            for row in data:
                st.write(row)
        else:
            st.error("Erreur lors de la récupération des données.")

        # Mise à jour des données
        st.subheader("Mettre à jour une entrée")
        id_update = st.number_input("ID de l'utilisateur à mettre à jour", min_value=1, step=1)
        nom_update = st.text_input("Nouveau Nom")
        email_update = st.text_input("Nouvel Email")
        age_update = st.number_input("Nouvel Âge", min_value=1, max_value=120, step=1)

        if st.button("Mettre à jour"):
            if id_update and nom_update and email_update and age_update:
                data_update = {
                    "id": id_update,
                    "nom": nom_update,
                    "email": email_update,
                    "age": age_update
                }
                response = requests.put(API_UPDATE_URL, json=data_update)

                if response.status_code == 200:
                    st.success("Mise à jour réussie !")
                else:
                    st.error("Erreur lors de la mise à jour.")
            else:
                st.warning("Veuillez remplir tous les champs.")
    else:
        st.error("Identifiants incorrects !")
