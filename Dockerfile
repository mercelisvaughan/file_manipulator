# ==========================================
# STAGE 1: Build Tailwind CSS
# ==========================================
FROM node:18-alpine AS tailwind-builder

WORKDIR /app

# Copy package.json and install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the project files to build CSS
COPY . .

# Build the CSS file (adjust path if yours is different)
# This generates 'static/css/output.css'
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify


# ==========================================
# STAGE 2: Python Production Image
# ==========================================
FROM python:3.11-slim

# Prevent Python from writing .pyc files & buffer stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies for Postgres (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files from your computer to the container
COPY . .

# COPY the compiled CSS from Stage 1 (The "Builder" Stage)
COPY --from=tailwind-builder /app/static/css/output.css ./static/css/output.css

# Run the collection of static files (WhiteNoise needs this)
RUN python manage.py collectstatic --noinput

# Expose the port (Railway uses $PORT, but we document 8000)
EXPOSE 8000

# Start Gunicorn
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT