import streamlit as st
import requests
import base64
from streamlit_drawable_canvas import st_canvas
from streamlit_option_menu import option_menu
from PIL import Image, UnidentifiedImageError
import io
import random

API_URL = "http://backend:8000"

def display_image_from_bytes(img_bytes):
    """
    Essaie d'ouvrir l'image à partir de bytes et retourne un objet PIL.Image.
    En cas d'erreur, renvoie None.
    """
    try:
        pil_img = Image.open(io.BytesIO(img_bytes))
        pil_img.verify()
        pil_img = Image.open(io.BytesIO(img_bytes))
        return pil_img
    except (UnidentifiedImageError, Exception) as e:
        st.error(f"Erreur lors de l'ouverture de l'image: {e}")
        return None

def app_non_auth():
    st.title("Dessinez une forme et obtenez une prédiction !")

    st.markdown("""
    **Instructions :**
    1. Dessinez une des formes suivantes sur le canvas :
    - **Cercle**
    - **Triangle**
    - **Carré**
    - **Pentagone**
    - **Hexagone**
    2. Cliquez sur **"Submit and Predict"** pour envoyer votre dessin au serveur.
    3. Le serveur analysera votre dessin et affichera la forme détectée.
    """)

    stroke_width = st.slider("Épaisseur du trait :", 1, 25, 3)
    stroke_color = st.color_picker("Couleur du trait :", "#000000")
    bg_color = st.color_picker("Couleur de fond :", "#FFFFFF")
    width, height = 300, 300

    drawing_mode = st.selectbox(
        "Outil de dessin :", ("freedraw", "line", "rect", "circle", "transform", "polygon")
    )

    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = "canvas_initial"

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Effacer"):
            st.session_state.canvas_key = f"canvas_{random.randint(1,10000)}"

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        key=st.session_state.canvas_key,
    )

    if st.button("Submit and Predict"):
        if canvas_result.image_data is not None:
            # Convertir le dessin en image et l'encoder en base64
            img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format="PNG")
            img_bytes = img_bytes_io.getvalue()
            b64_image = base64.b64encode(img_bytes).decode('utf-8')

            with open("image_front_new.png", "wb") as f:
                f.write(img_bytes)

            resp = requests.post(f"{API_URL}/predict", json={"image_base64": b64_image})
            st.write("Request sent")
            if resp.status_code == 200:
                predicted_shape = resp.json()["predicted_shape"]
                st.success(f"La forme prédite est : {predicted_shape}")
            else:
                st.error(f"Erreur durant la prédiction : {resp.text}")
        else:
            st.warning("Veuillez dessiner quelque chose avant de soumettre.")

    # Récupération des images (accessible à tous)
    resp = requests.get(f"{API_URL}/images")
    if resp.status_code != 200:
        st.error("Erreur lors de la récupération des images")
        return

    data = resp.json()
    st.subheader("Liste des images enregistrées")
    for record in data:
        with st.expander(f"Image ID: {record['id']} - Forme prédite : {record['predicted_shape']}"):
            b64_str = record["image_base64"]
            img_bytes = base64.b64decode(b64_str)
            pil_img = display_image_from_bytes(img_bytes)
            if pil_img is not None:
                st.image(pil_img, width=200)
            else:
                st.error("L'image n'a pas pu être affichée.")
            st.info("La modification des tags est réservée aux utilisateurs authentifiés.")

def app_auth():
    st.title("Visualisation et mise à jour des formes - Authentifié")

    token = st.session_state.get("token", None)
    if not token:
        st.warning("Vous n'êtes pas authentifié.")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_URL}/images", headers=headers)
    if resp.status_code != 200:
        st.error("Erreur lors de la récupération des images")
        return

    data = resp.json()
    
    cols = st.columns(4)
    for i, record in enumerate(data):
        with cols[i % 4]:
            b64_str = record["image_base64"]
            img_bytes = base64.b64decode(b64_str)
            pil_img = display_image_from_bytes(img_bytes)
            if pil_img is not None:
                st.image(pil_img, use_container_width=True)
                st.write(f"ID: {record['id']}")
                st.write(f"Prédit: {record['predicted_shape']}")
                new_shape = st.text_input("Nouvelle forme :", value=record["predicted_shape"], key=f"shape_{record['id']}")
                if st.button(f"Update_{record['id']}"):
                    update_resp = requests.put(
                        f"{API_URL}/update",
                        headers=headers,
                        json={"image_id": record['id'], "new_shape": new_shape}
                    )
                    if update_resp.status_code == 200:
                        st.success("Forme mise à jour")
                    else:
                        st.error("Erreur mise à jour")
            else:
                st.error("Image non affichée")

def login():
    st.title("Connexion")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        form_data = {
            "username": username,
            "password": password
        }
        resp = requests.post(
            f"{API_URL}/login", 
            data=form_data, 
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            st.session_state["token"] = token
            st.success("Connecté avec succès !")
            st.rerun()
        else:
            st.error("Identifiants invalides")

def main():
    selected = option_menu(
        menu_title="TD MLOps",
        options=["Home", "Page Admin"],
        icons=["house", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        app_non_auth()
    elif selected == "Page Admin":
        if "token" in st.session_state:
            app_auth()
        else:
            login()

if __name__ == "__main__":
    main()
