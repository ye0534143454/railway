import json
import os
import yt_dlp
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def download_video(url):
    options = {
        'outtmpl': 'video.mp4',
        'format': 'worst'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def upload_to_drive():
    # שלב 1: קרא את מחרוזת ה־JSON מתוך משתנה סביבה
    client_secrets_str = os.environ.get('CLIENT_SECRETS_JSON')
    if not client_secrets_str:
        raise ValueError("❌ משתנה הסביבה CLIENT_SECRETS_JSON לא מוגדר")

    # שלב 2: כתוב את המחרוזת לקובץ זמני
    with open("client_secrets.json", "w") as f:
        f.write(client_secrets_str)

    try:
        # שלב 3: התחברות לגוגל
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # שלב 4: העלאה לדרייב
        f = drive.CreateFile({'title': 'video.mp4'})
        f.SetContentFile('video.mp4')
        f.Upload()
        print("✅ הועלה ל־Drive בהצלחה")
    finally:
        # שלב 5: מחק את הקובץ הרגיש
        os.remove("client_secrets.json")

def main():
    url = os.environ.get("VIDEO_URL")
    if not url:
        raise ValueError("❌ משתנה הסביבה VIDEO_URL לא מוגדר")

    download_video(url)
    upload_to_drive()

if __name__ == "__main__":
    main()
