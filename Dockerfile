# Use Python base image
FROM python:3.13.3

# Set working directory
WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional pytest packages
RUN pip install --no-cache-dir \
    pytest-html \
    pytest-cov \
    pytest-selenium

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]