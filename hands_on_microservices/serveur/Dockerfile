# Use a lightweight Python image
FROM python:3.11-slim

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn psycopg2-binary pillow python-multipart transformers numpy torch
# Copy the application code
COPY main.py /app/main.py
COPY test.py /app/test.py
COPY image.png /app/image.png

WORKDIR /app
# Set the working directory to /app
# Expose UDS path as a volume
VOLUME ["/tmp"]
# Run Uvicorn using the Unix Domain Socket
# CMD ["uvicorn", "main:app", "--uds", "/tmp/serveur.sock", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

