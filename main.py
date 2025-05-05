import json
import os
import yt_dlp
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def get_video_info(url):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def download_video(url, filename):
    options = {
        'outtmpl': filename,
        'format': 'worst'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def upload_to_drive(local_filename, drive_filename):
    # קריאה ממחרוזת JSON שמכילה את האישורים
    credentials_json_str = os.environ.get('CREDENTIALS_JSON')
    if not credentials_json_str:
        raise ValueError("❌ משתנה הסביבה CREDENTIALS_JSON לא מוגדר")

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

        f = drive.CreateFile({'title': drive_filename})
        f.SetContentFile(local_filename)
        f.Upload()
        print(f"✅ '{drive_filename}' הועלה ל־Drive בהצלחה")

    finally:
        os.remove("credentials.json")

def sanitize_filename(title):
    # מסיר תווים בעייתיים לשמות קבצים
    import re
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', title)
    return sanitized

def main():
    url = os.environ.get("VIDEO_URL")
    if not url:
        raise ValueError("❌ משתנה הסביבה VIDEO_URL לא מוגדר")

    info = get_video_info(url)
    video_title = sanitize_filename(info.get("title", "video"))
    filename = f"{video_title}.mp4"

    download_video(url, filename)
    upload_to_drive(filename, filename)

    # אופציונלי: מחיקת הקובץ המקומי לאחר העלאה
    os.remove(filename)

if __name__ == "__main__":
    main()
