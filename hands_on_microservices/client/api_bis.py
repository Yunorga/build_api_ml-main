import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
from io import BytesIO
from PIL import Image
import json
import pandas as pd


# URL de l'API
API_IMG_UPLOAD_URL = "http://serveur:8000/img_upload"
API_PREDICT_URL = "http://serveur:8000/predict_shape"
API_GET_ALL_IMAGES = "http://serveur:8000/all_img"
API_EXECUTE_SQL = "http://serveur:8000/execute_sql"

st.set_page_config(page_title="Reconnaissance de formes", layout="centered")

st.title("🖌️ Dessinez une forme et obtenez une super prédiction !")

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
stroke_color = st.color_picker("Couleur du trait :")
bg_color = st.color_picker("Couleur de fond :", "#FFFFFF")

width, height = 300, 300  

drawing_mode = st.selectbox(
    "Outil de dessin :", ("freedraw", "line", "rect", "circle", "transform", "polygon")
)

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode=drawing_mode,
    key="canvas",
)

if st.button("Submit and Predict"):
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        response = requests.post(API_PREDICT_URL, files={"file": ("image.png", img_bytes, "image/png")})

        if response.status_code == 200:
            prediction = response.json().get("shape", "Inconnue")
            st.success(f"✅ Forme détectée : **{prediction}**")
        else:
            st.error(f"❌ Erreur lors de la prédiction : {response.text}")
    else:
        st.warning("⚠️ Veuillez dessiner une forme avant de soumettre.")

if st.button("Get all images"):
    response = requests.get(API_GET_ALL_IMAGES)

    if response.status_code == 200:
        images_base64 = json.loads(response.content)["images"]
        
        cols = st.columns(3)
        
        print(response.content)

        for i, img_data in enumerate(images_base64):
            image = Image.open(BytesIO(img_data))
            cols[i % 3].image(image, use_column_width=True)
    else:
        st.error("❌ Erreur lors de la récupération des images.")


st.subheader("🔍 Exécuter une requête SQL sur la base de données")

# Champ de saisie pour entrer une requête SQL
query = st.text_area("Entrez votre requête SQL ici", value="SELECT * FROM images LIMIT 1")

if st.button("Exécuter la requête SQL"):
    response = requests.post(API_EXECUTE_SQL, data={"query": query})

    if response.status_code == 200:
        result = response.json().get("result", "")

        if isinstance(result, list):  # Si c'est une liste (résultats SELECT)
            if result:
                df = pd.DataFrame(result)
                st.dataframe(df)  # Affichage sous forme de tableau
            else:
                st.info("✅ Requête exécutée avec succès mais aucun résultat.")
        else:  # Si c'est un message de confirmation
            st.success(result)
    else:
        st.error(f"❌ Erreur SQL : {response.json().get('detail', 'Erreur inconnue')}")


if st.button("Image"):
    response = requests.put(API_GET_ALL_IMAGES)
    # image = Image.open(BytesIO(response.content))
    image = Image.open(response.content)
    st.image(image)

# # Section pour exécuter une requête SQL sur la base de données
# st.subheader("🔍 Exécuter une requête SQL sur la base de données")
# query = st.text_area("Entrez votre requête SQL ici", value="SELECT * FROM utilisateurs LIMIT 5")
# if st.button("Exécuter la requête SQL"):
#     response = requests.post(API_EXECUTE_SQL, data={"query": query})
#     if response.status_code == 200:
#         result = response.json().get("result", "")
#         if isinstance(result, list):
#             df = pd.DataFrame(result)
#             st.dataframe(df)
#         else:
#             st.success(result)
#     else:
#         st.error(f"Erreur SQL : {response.text}")


# # 📌 Section pour exécuter une requête SQL
# st.subheader("🔍 Exécuter une requête SQL sur la base de données")
# query = st.text_area("Entrez votre requête SQL ici", value="SELECT * FROM utilisateurs LIMIT 5")
# if st.button("Exécuter la requête"):
#     response = requests.post(API_EXECUTE_SQL, data={"query": query})
#     result = response.json()

#     if "error" in result:
#         st.error(result["error"])
#     else:
#         if isinstance(result["result"], list):
#             df = pd.DataFrame(result["result"])
#             st.dataframe(df)
#         else:
#             st.success(result["result"])


# import streamlit as st
# from streamlit_drawable_canvas import st_canvas
# import requests
# from io import BytesIO
# from PIL import Image

# # URL de l'API
# API_IMG_UPLOAD_URL = "http://serveur:8000/img_upload"
# API_PREDICT_URL = "http://serveur:8000/predict_shape"

# st.set_page_config(page_title="Reconnaissance de formes", layout="centered")

# st.title("🖌️ Dessinez une forme et obtenez une super prédiction !")

# # 🎯 Instructions pour l'utilisateur
# st.markdown(
#     """
#     **Instructions :**
#     1. Dessinez une des formes suivantes sur le canvas :
#        - **Cercle**
#        - **Triangle**
#        - **Carré**
#        - **Pentagone**
#        - **Hexagone**
#     2. Cliquez sur **"Submit and Predict"** pour envoyer votre dessin au serveur.
#     3. Le serveur analysera votre dessin et affichera la forme détectée.
#     """
# )

# # 🎨 Paramètres du canvas
# stroke_width = st.slider("Épaisseur du trait :", 1, 25, 3)
# stroke_color = st.color_picker("Couleur du trait :")
# bg_color = st.color_picker("Couleur de fond :", "#FFFFFF")

# width, height = 300, 300  # Taille du canvas

# # 📜 Sélection du mode de dessin
# drawing_mode = st.selectbox(
#     "Outil de dessin :", ("freedraw", "line", "rect", "circle", "transform", "polygon")
# )

# # 🖍️ Création du canvas
# canvas_result = st_canvas(
#     fill_color="rgba(255, 165, 0, 0.3)",
#     stroke_width=stroke_width,
#     stroke_color=stroke_color,
#     background_color=bg_color,
#     update_streamlit=True,
#     height=height,
#     width=width,
#     drawing_mode=drawing_mode,
#     key="canvas",
# )

# # 📤 Bouton pour soumettre le dessin
# if st.button("Submit and Predict"):
#     if canvas_result.image_data is not None:
#         # Convertir le dessin en image
#         img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
#         img_bytes = BytesIO()
#         img.save(img_bytes, format="PNG")
#         img_bytes = img_bytes.getvalue()

#         # Envoyer l'image au serveur pour prédiction
#         response = requests.post(API_PREDICT_URL, files={"file": ("image.png", img_bytes, "image/png")})

#         if response.status_code == 200:
#             prediction = response.json().get("shape", "Inconnue")
#             st.success(f"✅ Forme détectée : **{prediction}**")
#         else:
#             st.error(f"❌ Erreur lors de la prédiction : {response.text}")
#     else:
#         st.warning("⚠️ Veuillez dessiner une forme avant de soumettre.")
        

# if st.button("Get all images"):
#     response = requests.get("http://serveur:8000/all_img")
#     if response.status_code == 200:
#         images = response.content
#         for i, img in enumerate(images):
#             image = Image.open(BytesIO(img))
#             st.image(image)
#     else:
#         st.error("Erreur lors de la récupération des données.")