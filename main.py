import json
import os
import yt_dlp
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def download_video(url):
    options = {
        'outtmpl': 'video.mp4',
        'format': 'worst'  # איכות הכי נמוכה
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def upload_to_drive():
    # קריאה ממחרוזת JSON שמכילה את האישורים (credentials.json)
    credentials_json_str = os.environ.get('CREDENTIALS_JSON')
    if not credentials_json_str:
        raise ValueError("❌ משתנה הסביבה CREDENTIALS_JSON לא מוגדר")

    # שמירת הקובץ credentials.json לקובץ זמני
    with open("credentials.json", "w") as f:
        json.dump(json.loads(credentials_json_str), f)

    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("credentials.json")

        if gauth.credentials is None:
            raise RuntimeError("❌ credentials.json לא תקף")
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        drive = GoogleDrive(gauth)

        f = drive.CreateFile({'title': 'video.mp4'})
        f.SetContentFile('video.mp4')
        f.Upload()
        print("✅ הועלה ל־Drive בהצלחה")

    finally:
        os.remove("credentials.json")  # מחיקת הקובץ הרגיש

def main():
    url = os.environ.get("VIDEO_URL")
    if not url:
        raise ValueError("❌ משתנה הסביבה VIDEO_URL לא מוגדר")

    download_video(url)
    upload_to_drive()

if __name__ == "__main__":
    main()
