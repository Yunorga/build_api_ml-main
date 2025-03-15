import base64
from PIL import Image
import io
import random
import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch


# SHAPES = ["circle", "square", "triangle", "star", "heart"]

SHAPES = ["None", "Circle", "Triangle", "Square", "Pentagon", "Hexagon"]
MODEL_NAME = "0-ma/vit-geometric-shapes-tiny"

try:
    feature_extractor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")

def predict_shape_from_base64(image_base64: str) -> str:
    """
    Décode l'image base64 et utilise un modèle de machine learning 
    pour prédire la forme.
    """
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_base64))).convert("RGB")
        inputs = feature_extractor(images=image, return_tensors="pt")
        
        with torch.no_grad(): # Important pour l'inference.
            logits = model(**inputs).logits.detach().cpu().numpy()

        prediction = np.argmax(logits, axis=1)[0]
        predicted_label = SHAPES[prediction]
        return predicted_label
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return "Erreur"

