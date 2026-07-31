# Use official Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python output buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
# build-essential already includes gcc, libpq-dev is for psycopg2,
# libjpeg-dev/zlib1g-dev are for Pillow (passport photos, event banners)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first (layer caching — only reinstalls deps when this file changes)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django port — matches docker-compose.yml's "8000:8000" mapping
EXPOSE 8000

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Start Django — overridden by docker-compose.yml's `command:` in dev,
# this is the fallback if the image is ever run standalone
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]