import streamlit as st
import requests

# URL de l'API FastAPI accessible depuis le conteneur Streamlit.
# Ici, on suppose que le conteneur backend est nommé "backend" et écoute sur le port 8000.
API_URL = "http://backend:8000"

st.title("Test de l'API pour la classification d'issues")

st.write("""
Entrez le texte de l'issue ci-dessous.
""")

# Zone de saisie pour le texte de l'issue
text_input = st.text_area("Texte de l'issue", "", height=200)

if st.button("Prédire"):
    # if not text_input.strip():
    #     st.error("Veuillez entrer du texte avant de lancer la prédiction.")
    # else:
    payload = {"text": text_input}
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Résultats de l'inférence")
            st.write("Logits :", result.get("logits"))
            st.write("Labels prédits :", result.get("predicted_labels"))
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API: {str(e)}")



# --- NEW CODE  ---

# import streamlit as st
# import requests
# import os

# API_URL = "http://backend:8000"  # Utilisation du nom de service dans docker-compose

# # Initialisation des clés dans st.session_state
# if "token" not in st.session_state:
#     st.session_state["token"] = ""
# if "username" not in st.session_state:
#     st.session_state["username"] = ""

# # Vérifier si nous sommes en mode test via la variable d'environnement (pour le développement)
# TEST_MODE = True  # Remplacer par : os.getenv("TEST_MODE", "false").lower() == "true"

# # --- Définition des différentes pages de l'application ---

# def show_home():
#     st.title("Bienvenue sur GitHub Issue Classifier")
#     st.write("""
#     Ce service vous permet d'analyser les issues d'un repository GitHub et de prédire automatiquement des labels (ex. : Bug, Feature, Question).
#     Utilisez le menu de gauche pour naviguer entre les pages : Inscription, Connexion, Analyse et À propos.
#     """)

# def show_register():
#     st.title("Inscription")
#     username = st.text_input("Email", key="reg_username")
#     full_name = st.text_input("Nom complet", key="reg_fullname")
#     password = st.text_input("Mot de passe", type="password", key="reg_password")
#     if st.button("S'inscrire"):
#         if username and password:
#             payload = {"username": username, "full_name": full_name}
#             response = requests.post(API_URL + "/register", params={"password": password}, json=payload)
#             if response.status_code == 200:
#                 st.success("Inscription réussie ! Vous pouvez maintenant vous connecter.")
#             else:
#                 st.error("Erreur : " + response.text)
#         else:
#             st.warning("Veuillez remplir tous les champs.")

# def show_login():
#     st.title("Connexion")
#     username = st.text_input("Email", key="login_email")
#     password = st.text_input("Mot de passe", type="password", key="login_password")
#     if st.button("Se connecter"):
#         if username and password:
#             data = {"username": username, "password": password}
#             response = requests.post(API_URL + "/token", data=data)
#             if response.status_code == 200:
#                 token = response.json()["access_token"]
#                 st.session_state["token"] = token
#                 st.session_state["username"] = username
#                 st.success("Connexion réussie !")
#             else:
#                 st.error("Échec de la connexion : " + response.text)
#         else:
#             st.warning("Veuillez remplir tous les champs.")

# def show_logout():
#     if st.button("Se déconnecter"):
#         st.session_state["token"] = ""
#         st.session_state["username"] = ""
#         st.success("Déconnexion réussie.")

# def show_analyze():
#     st.title("Analyse d'un Repository GitHub")
#     if not st.session_state.get("token") and not TEST_MODE:
#         st.warning("Veuillez vous connecter d'abord.")
#         return
#     repo_url = st.text_input("Entrez l'URL du repository GitHub (ex. : https://github.com/owner/repo)")
#     if st.button("Analyser"):
#         # En mode test, on peut utiliser un token fictif
#         token = st.session_state.get("token", "") if not TEST_MODE else "test-token"
#         headers = {"Authorization": f"Bearer {token}"}
#         payload = {"repo_url": repo_url}
#         response = requests.post(API_URL + "/analyze", json=payload, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             st.markdown(f"## Résultats pour le repository : {data['repository']}")
#             for result in data["results"]:
#                 st.markdown(f"### {result['title']}")
#                 st.write("Labels prédits : " + ", ".join(result["labels"]))
#         else:
#             st.error("Erreur : " + response.text)

# def show_about():
#     st.title("À propos")
#     st.write("""
#     GitHub Issue Classifier est un service qui analyse les issues d'un repository GitHub et propose automatiquement des labels pertinents.
#     Le projet repose sur un modèle de classification multi-label, dont le suivi et l'optimisation s'inscrivent dans une démarche MLOps.
#     """)

# # --- Navigation via le menu latéral ---
# st.sidebar.title("Menu")
# page = st.sidebar.radio("Navigation", ["Accueil", "Inscription", "Connexion", "Analyser", "À propos"])

# if page == "Accueil":
#     show_home()
# elif page == "Inscription":
#     show_register()
# elif page == "Connexion":
#     show_login()
#     # Affichage de l'état de connexion et possibilité de se déconnecter
#     if st.session_state.get("token"):
#         st.sidebar.write(f"Connecté en tant que : {st.session_state.get('username')}")
#         show_logout()
# elif page == "Analyser":
#     show_analyze()
# elif page == "À propos":
#     show_about()


# --------------------  OLD CODE  --------------------

# import streamlit as st
# import requests
# import os

# API_URL = "http://backend:8000"  # Utilisation du nom de service dans docker-compose

# # Initialisation de st.session_state
# if "token" not in st.session_state:
#     st.session_state["token"] = ""

# # Vérifier si nous sommes en mode test via la variable d'environnement
# TEST_MODE = True #os.getenv("TEST_MODE", "false").lower() == "true"

# st.title("GitHub Issue Classifier")
# menu = ["Login", "Register", "Analyser un Repository"]
# choice = st.sidebar.selectbox("Menu", menu)

# if choice == "Register":
#     st.subheader("Inscription")
#     username = st.text_input("Email")
#     full_name = st.text_input("Nom complet")
#     password = st.text_input("Mot de passe", type="password")
#     if st.button("S'inscrire"):
#         payload = {"username": username, "full_name": full_name}
#         response = requests.post(API_URL + "/register", params={"password": password}, json=payload)
#         if response.status_code == 200:
#             st.success("Inscription réussie !")
#         else:
#             st.error("Erreur : " + response.text)

# if choice == "Login":
#     st.subheader("Connexion")
#     username = st.text_input("Email", key="login_email")
#     password = st.text_input("Mot de passe", type="password", key="login_password")
#     if st.button("Se connecter"):
#         data = {"username": username, "password": password}
#         response = requests.post(API_URL + "/token", data=data)
#         if response.status_code == 200:
#             token = response.json()["access_token"]
#             st.session_state["token"] = token  # Stockage du token
#             st.success("Connexion réussie !")
#         else:
#             st.error("Échec de la connexion : " + response.text)

# if choice == "Analyser un Repository":
#     st.subheader("Analyse d'un Repository GitHub")
#     # Si en mode test, on ne vérifie pas la présence d'un token
#     if not st.session_state.get("token") and not TEST_MODE:
#         st.warning("Veuillez vous connecter d'abord.")
#     else:
#         repo_url = st.text_input("Entrez l'URL du repository GitHub (ex. : https://github.com/owner/repo)")
#         if st.button("Analyser"):
#             # En mode test, on peut définir un token fictif
#             token = st.session_state.get("token", "") if not TEST_MODE else "test-token"
#             headers = {"Authorization": f"Bearer {token}"}
#             payload = {"repo_url": repo_url}
#             response = requests.post(API_URL + "/analyze", json=payload, headers=headers)
#             if response.status_code == 200:
#                 data = response.json()
#                 st.write(f"Résultats pour le repository : {data['repository']}")
#                 for result in data["results"]:
#                     # st.write(f"### {result['title']}")
#                     st.markdown(f"### {result['title']} [link]({result['url']}) ")# % url)
#                     st.write("Labels prédits : " + ", ".join(result["labels"]))
#             else:
#                 st.error("Erreur : " + response.text)
