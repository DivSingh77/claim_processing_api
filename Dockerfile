FROM python:3.9
WORKDIR /app
COPY backend /app/backend
RUN pip install fastapi uvicorn loguru sqlite3 sqlalchemy prometheus_client jwt
CMD ["uvicorn", "backend.routes:app", "--host", "0.0.0.0", "--port", "8000"]
