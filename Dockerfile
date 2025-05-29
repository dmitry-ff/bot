FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV BOT_TOKEN=001.0852096893.0629123419:1011881519
ENV MONGODB_URI=mongodb://mongodb:27017
ENV MONGODB_NAME=gratitude
CMD ["python", "main.py"]