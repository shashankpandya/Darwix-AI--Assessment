FROM python:3.11-slim

# Install ffmpeg (required by pydub)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure the audio output directory exists
RUN mkdir -p static/output

# HuggingFace Spaces expects port 7860
EXPOSE 7860

CMD ["python", "app.py"]
