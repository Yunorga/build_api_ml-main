from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from db_models import ImageRecord
from schemas import PredictRequest, PredictResponse, UpdateShapeRequest, UserAuth, TokenResponse
from ml_model import predict_shape_from_base64
from auth import authenticate_user, create_access_token, get_current_user

import base64

# Crée la base de données (tables) au démarrage si non existantes
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dépendance pour obtenir la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint de login pour obtenir un token JWT
@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return TokenResponse(access_token=access_token)

# Endpoint pour prédire la forme d'une image accessible par tous
@app.post("/predict", response_model=PredictResponse)
def predict_shape(request: PredictRequest, db: Session = Depends(get_db)):

    print(f"Received image with {len(request.image_base64)} bytes\n")

    # 1) On prédit la forme avec un modèle
    predicted_shape = predict_shape_from_base64(request.image_base64)
    # predicted_shape = "circle"

    print(f"Predicted shape: {predicted_shape}\n")

    # 2) On stocke l'image et la forme prédite dans la DB
    image_data = base64.b64decode(request.image_base64)

    # Exemple : sauvegarde locale (pour débogage, à adapter en production)
    with open("image.png", "wb") as f:
        f.write(image_data)

    image_record = ImageRecord(
        image_data=image_data,
        predicted_shape=predicted_shape
    )

    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    # 3) On renvoie la forme prédite
    return PredictResponse(predicted_shape=predicted_shape)

# Endpoint pour récupérer la liste des images et formes prédites uniquement pour les utilisateurs authentifiés
@app.get("/images")
def get_all_images(db: Session = Depends(get_db)):
    # Récupère tous les enregistrements
    images = db.query(ImageRecord).all()
    # Convertit le binaire en base64 pour l'envoi
    results = []
    for img in images:
        b64_str = base64.b64encode(img.image_data).decode('utf-8')
        results.append({
            "id": img.id,
            "image_base64": b64_str,
            "predicted_shape": img.predicted_shape
        })
    return results

# Endpoint pour mettre à jour la forme prédite d'une image uniquement pour les utilisateurs authentifiés

@app.put("/update")
def update_image_shape(request: UpdateShapeRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    image_record = db.query(ImageRecord).filter(ImageRecord.id == request.image_id).first()
    if not image_record:
        raise HTTPException(status_code=404, detail="Image not found")

    image_record.predicted_shape = request.new_shape
    db.commit()
    db.refresh(image_record)
    return {"message": "Shape updated successfully", "updated_shape": image_record.predicted_shape}
