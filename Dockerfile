# השתמש בבסיס פייתון
FROM python:3.11-slim

# צור תיקיית עבודה
WORKDIR /app

# העתק את הדרישות קודם - שלב זה ינצל cache אם הדרישות לא השתנו
COPY requirements.txt .

# התקן את התלויות
RUN pip install --upgrade pip && pip install -r requirements.txt

# עכשיו העתק את שאר הקוד
COPY . .

# הפקודה שתורץ כשמפעילים את הקונטיינר
CMD ["python", "main.py"]
