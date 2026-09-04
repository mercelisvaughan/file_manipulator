# ==========================================
# STAGE 1: Build Tailwind CSS
# ==========================================
FROM node:18-alpine AS tailwind-builder

WORKDIR /app

# Copy package.json and install Node dependencies
COPY package*.json ./
RUN npm install

# Copy project files to build CSS
COPY . .

# Build the minified CSS output
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify


# ==========================================
# STAGE 2: Python Production Image
# ==========================================
# Use Python 3.12 to satisfy Django 6.1.1 requirements
FROM python:3.12-slim

# Modern ENV syntax (ENV key=value)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for Postgres (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Copy compiled CSS from Stage 1
COPY --from=tailwind-builder /app/static/css/output.css ./static/css/output.css

# Run collectstatic with dummy build-time environment variables
# WhiteNoise compiles assets here without needing live production secrets
RUN SECRET_KEY=build-time-insecure-secret-key python manage.py collectstatic --noinput

# Expose port (Railway dynamically injects $PORT at runtime)
EXPOSE 8000

# Start Gunicorn via shell execution so $PORT expands dynamically
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]