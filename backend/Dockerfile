FROM python:3.12-slim

# Install nodejs and npm
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy js-analyzer and install deps
COPY js-analyzer/ /js-analyzer/
RUN cd /js-analyzer && npm install

# Copy backend application
COPY backend/ .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}"]
