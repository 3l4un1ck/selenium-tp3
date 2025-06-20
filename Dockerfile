FROM python:3.13.3

WORKDIR /app

# Install sqlite3 if not already present
RUN apt-get update && apt-get install -y sqlite3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install test dependencies
RUN pip install --no-cache-dir \
    pytest-html \
    pytest-cov \
    pytest-selenium

COPY . .

ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]