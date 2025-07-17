# 1. Folosim o imagine oficială Python ca bază
FROM python:3.10-slim

# 2. Setăm un director de lucru în interiorul containerului
WORKDIR /app

# 3. Copiem fișierul cu dependințe
COPY requirements.txt requirements.txt

# 4. Instalăm dependințele
# Folosim --no-cache-dir pentru a păstra imaginea cât mai mică
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiem restul fișierelor din proiect în container
COPY . .

# 6. Expunem portul pe care va rula aplicația în container.
# Gunicorn va rula pe portul 8000.
EXPOSE 8000

# 7. Comanda care va porni aplicația când pornește containerul.
# Folosim Gunicorn, serverul de producție.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--worker-tmp-dir", "/dev/shm", "app:app"]
