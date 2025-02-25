# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install the backend package in editable mode to pick up pyproject.toml configuration
RUN pip install -e .

# Copy the backend source code
COPY . /app/

EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
