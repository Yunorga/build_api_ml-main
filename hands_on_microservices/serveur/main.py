from fastapi import FastAPI, File, HTTPException, Response, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from io import BytesIO
from PIL import Image
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import uvicorn
import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch

app = FastAPI()

# 📌 Chargement unique du modèle et du feature extractor
labels = ["None", "Circle", "Triangle", "Square", "Pentagon", "Hexagon"]
MODEL_NAME = "0-ma/vit-geometric-shapes-tiny"

try:
    feature_extractor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
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

# Route principale
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}

# 📌 Route pour récupérer toutes les images sous forme de liste binaire
@app.get("/all_img")
def get_all_images():
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT image FROM images")  # Récupère toutes les images
        data = cur.fetchall()
        cur.close()
        conn.close()

        
        if not data:
            raise HTTPException(status_code=404, detail="Aucune image trouvée.")

        
        images = [img["image"] for img in data]
        
        print("----"*20)
        
        return Response(content=data[0]["image"], media_type="image/png")
        # return #Response(content=images, media_type="application/octet-stream")
    # return {"images": [BytesIO(img).getvalue() for img in images]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des images : {e}")



# 📌 Route pour sauvegarder une image dans PostgreSQL
@app.post("/img_upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        logging.info(f"Fichier reçu : {file.filename}, Type : {file.content_type}")

        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=415, detail="Format d'image non supporté. Utilisez PNG ou JPEG.")
        
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))


        if image.format not in ["PNG", "JPEG"]:
            raise HTTPException(status_code=400, detail="Fichier invalide. Format d'image incorrect.")

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

# 📌 Route pour la prédiction des formes
@app.post("/predict_shape")
async def predict_shape(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=415, detail="Format d'image non supporté. Utilisez PNG ou JPEG.")

        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        inputs = feature_extractor(images=image, return_tensors="pt")

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO images (image) VALUES (%s)", (psycopg2.Binary(image_bytes),))
                conn.commit()

        with torch.no_grad():
            logits = model(**inputs).logits.cpu().numpy()

        prediction = np.argmax(logits, axis=1)[0]
        predicted_label = labels[prediction]

        return {"shape": predicted_label}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")


@app.post("/execute_sql")
def execute_sql(query: str = Form(...)):
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute(query)

        # Vérifier si la requête est un SELECT pour récupérer les données
        if query.strip().lower().startswith("select"):
            data = cur.fetchall()
        else:
            conn.commit()
            data = "Requête exécutée avec succès"

        cur.close()
        conn.close()

        return jsonable_encoder({"result": data})

    except Exception as e:
        return {"detail": f"Erreur SQL : {str(e)}"}


# 🔹 Route pour exécuter une requête SQL arbitraire depuis le frontend
# @app.post("/execute_sql")
# def execute_sql(query: str = Form(...)):
#     try:
#         conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         cur.execute(query)
#         # Si la requête commence par SELECT, on récupère les données
#         if query.strip().lower().startswith("select"):
#             # Conversion explicite de chaque ligne en dictionnaire
#             data = [dict(row) for row in cur.fetchall()]
#         else:
#             data = None
#         conn.commit()
#         cur.close()
#         conn.close()

#         result = data if data is not None else "Requête exécutée avec succès"
#         return jsonable_encoder({"result": result})

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erreur SQL : {e}")



# # 📌 Route pour exécuter une requête SQL personnalisée
# @app.post("/execute_sql")
# def execute_sql(query: str = Form(...)):
#     try:
#         conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         cur.execute(query)
#         data = cur.fetchall() if query.lower().startswith("select") else None
#         conn.commit()
#         cur.close()
#         conn.close()

#         return {"result": data if data else "Requête exécutée avec succès"}

#     except Exception as e:
#         return {"error": f"Erreur SQL : {e}"}


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
