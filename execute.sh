#!/bin/bash

set -e

echo "🧱 Building and starting containers..."
docker-compose up -d --build

echo "⏱ Waiting for web app to be ready..."
sleep 10  # à ajuster si nécessaire

#echo "🧪 Running unit tests (Pytest)..."
#docker-compose run --rm pytest

# Ajoutez ici une commande équivalente pour les tests Selenium si vous avez un dossier séparé
#  docker-compose run --rm selenium-tests

echo "📄 Reports should be available in the reports/ folder."

# Optionnel : arrêter les services après les tests
#docker-compose down
