FROM python:3.11-slim

WORKDIR /app

# התקנת ffmpeg (וחבילות מינימליות שצריך כדי שהוא ירוץ)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# התקנת חבילות פייתון
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# העתקת קוד הפרויקט
COPY . .

# הפעלת הקוד הראשי
CMD ["python", "main.py"]
