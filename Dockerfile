# 1. Folosim o imagine oficială Python ca bază
FROM python:3.10-slim

# 2. Setăm un director de lucru în interiorul containerului
WORKDIR /app

# 3. Copiem fișierul cu dependințe
COPY requirements.txt requirements.txt

# 4. Instalăm dependințele
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiem restul fișierelor din proiect în container
COPY . .

# 6. Comanda care va porni aplicația (format "shell" pentru a înlocui $PORT)
CMD gunicorn --bind 0.0.0.0:$PORT --worker-tmp-dir /dev/shm app:app
