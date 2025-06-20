# Stage 1: Build and test
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run unit tests and coverage
RUN pytest --cov=. --cov-report=html

RUN pytest --cov=app tests/ --junitxml=test-results.xml

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]