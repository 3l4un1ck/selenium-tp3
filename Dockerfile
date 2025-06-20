FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y curl chromium-driver chromium && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

# Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Variables d’environnement Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
