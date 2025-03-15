# Utilise une image Python
FROM python:3.9-slim

# Créer un dossier /app
WORKDIR /app

# Copier requirements et installer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code dans /app
COPY . /app

# Exposer le port 8000
EXPOSE 8000

# Démarrer l'application FastAPI via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
