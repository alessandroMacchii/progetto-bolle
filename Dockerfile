# Immagine per la prova online. In locale si continua a usare
# "Avvia carico merci.bat"; questo serve solo all'hosting.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BOLLE_HOST=0.0.0.0 \
    PORT=8000 \
    BOLLE_DATA_DIR=/data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bolle/ bolle/
COPY config/ config/
COPY gold/ gold/

# /data e' il volume persistente: database, scansioni caricate, export
VOLUME /data
EXPOSE 8000
CMD ["python", "-m", "bolle.app"]
