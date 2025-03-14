# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory to /app

# Install FastAPI, Uvicorn, and httpx
RUN pip install fastapi uvicorn httpx streamlit streamlit_extras pillow streamlit_drawable_canvas
# Copy the application code
COPY api_bis.py /app/api_bis.py
COPY pages /app/pages
# COPY /pages/*.py /app/pages/*

WORKDIR /app

# Expose UDS path as a volume
# VOLUME ["/tmp"]
# Run Uvicorn
# CMD ["uvicorn", "api.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["streamlit", "run", "api.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
CMD ["streamlit", "run", "api_bis.py",  "--server.port", "8501", "--server.address", "0.0.0.0"]