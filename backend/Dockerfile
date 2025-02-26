# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy the root-level requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install production dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install the backend package in editable mode from the 'backend' folder
RUN pip install -e backend

# Copy the entire repository into the container
COPY . /app/

EXPOSE 8000

# Run migrations and start the Django server using the backend's manage.py
CMD ["sh", "-c", "python backend/manage.py migrate && python backend/manage.py runserver 0.0.0.0:8000"]
