from fastapi import FastAPI,File, HTTPException, Depends, Response, UploadFile
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import logging
import uvicorn

import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch

app = FastAPI()

# 📌 Chargement unique du modèle et du feature extractor
labels = [
    "None",
    "Circle",
    "Triangle",
    "Square",
    "Pentagon",
    "Hexagon"
]
MODEL_NAME = "0-ma/vit-geometric-shapes-tiny"

try:
    feature_extractor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()  # Mode évaluation
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")



# Connexion à PostgreSQL
DB_CONFIG = {
    "dbname": "my_database",
    "user": "postgres",
    "password": "12345678",
    "host": "postgres",
    "port": "5432"
}

app = FastAPI()

# Modèle de données
class DataModel(BaseModel):
    nom: str
    email: str
    age: int

class UpdateDataModel(BaseModel):
    id: int
    nom: str
    email: str
    age: int

# Route principale
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}

# Route pour insérer des données (utilisateur)
@app.post("/insert")
def insert_data(data: DataModel):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = "INSERT INTO utilisateurs (nom, email, age) VALUES (%s, %s, %s)"
        cur.execute(query, (data.nom, data.email, data.age))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Données insérées avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour récupérer les données (admin)
@app.get("/get_all", response_model=List[dict])
def get_all_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour mettre à jour des données (admin)
@app.put("/update")
def update_data(data: UpdateDataModel):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = "UPDATE utilisateurs SET nom=%s, email=%s, age=%s WHERE id=%s"
        cur.execute(query, (data.nom, data.email, data.age, data.id))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Données mises à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/img")
def send_image():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        # cur.execute("SELECT * FROM images limit 1 where id = 1")
        cur.execute("SELECT * FROM images")# ORDER BY id DESC LIMIT 1")
        data = cur.fetchall()
        cur.close()
        conn.close()

        print(data)
        return Response(content=data[0]["image"], media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/img_upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        logging.info(f"Fichier reçu : {file.filename}, Type : {file.content_type}")

        # Vérifier le type du fichier
        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=415, detail="Format d'image non supporté. Utilisez PNG ou JPEG.")

        # Lecture du fichier
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Vérifier si l'image est valide
        if image.format not in ["PNG", "JPEG"]:
            raise HTTPException(status_code=400, detail="Fichier invalide. Format d'image incorrect.")

        # Option 1 : Sauvegarde locale
        image.save(f"uploaded_{file.filename}")

        # Option 2 : Sauvegarde dans PostgreSQL (BLOB)
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO images (image) VALUES (%s)", (psycopg2.Binary(image_bytes),))
                conn.commit()

        logging.info("Image enregistrée avec succès")
        return {"message": "Image uploadée et enregistrée avec succès"}

    except HTTPException as e:
        logging.error(f"Erreur HTTP : {e.detail}")
        raise e

    except Exception as e:
        logging.error(f"Erreur serveur : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# @app.put("/img_upload")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         logging.info(f"Received file: {file.filename}, content type: {file.content_type}") #Log
#         if file.content_type != "image/png":
#             raise HTTPException(status_code=415, detail="Unsupported media type")
#         image_bytes = await file.read()
#         image = Image.open(BytesIO(image_bytes))
#         image.save("received_image.png")
#         logging.info("Image saved successfully") #Log
#         return {"message": "Image uploaded successfully"}
#     except HTTPException as e:
#         logging.error(f"HTTPException : {e.detail}")
#         raise e
#     except Exception as e:
#         logging.error(f"Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/all_img")
def get_all_images():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT * FROM images")
        data = cur.fetchall()
        cur.close()
        conn.close()

        print(data)

        content = []
        for i in range(len(data)):
            content.append(data[i]["image"])
        return Response(content=content, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # return Response(content=data[0]["image"], media_type="image/png")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    
# example of how to use the API to get all images
# import requests
# response = requests.get("http://localhost:8000/all_img")
# images = response.content
# for i, img in enumerate(images):
#     with open(f"image_{i}.png", "wb") as f:
#         f.write(img)

@app.post("/predict_shape")
async def predict_shape(file: UploadFile = File(...)):
    try:
        # Vérifier que le fichier est bien une image
        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=415, detail="Format d'image non supporté. Utilisez PNG ou JPEG.")

        # Chargement de l'image
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Extraction des features
        inputs = feature_extractor(images=image, return_tensors="pt")

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO images (image) VALUES (%s)", (psycopg2.Binary(image_bytes),))
                conn.commit()

        # Prédiction
        with torch.no_grad():
            logits = model(**inputs).logits.cpu().numpy()

        prediction = np.argmax(logits, axis=1)[0]  # Récupérer la classe prédite
        predicted_label = labels[prediction]

        return {"shape": predicted_label}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# @app.put("/img_upload")
# def upload_image(image: bytes):
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cur = conn.cursor()
#         query = "INSERT INTO images (image) VALUES (%s)"
#         cur.execute(query, (image,))
#         conn.commit()
#         cur.close()
#         conn.close()    
#         return {"message": "Image insérée avec succès"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str)




# give an example of how to use the API
# to upload an image 

# import requests
# import streamlit as st
# from PIL import Image
# import io

# image = Image.open("image.png")
# image_bytes = io.BytesIO()
# # image.save(image_bytes, format="PNG")
# # image_bytes = image_bytes.getvalue()
# image = open("image.png", "rb").read()
# response = requests.put("http://localhost:8000/img_upload", data=image)
    
