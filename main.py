import yt_dlp
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def download_video(url):
    options = {
        'outtmpl': 'video.mp4',
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    print("✅ הסרטון ירד בהצלחה!")

def upload_to_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    f = drive.CreateFile({'title': 'video.mp4'})
    f.SetContentFile('video.mp4')
    f.Upload()
    print("✅ הועלה ל־Drive בהצלחה")

def main():
    url = input("🔗 הכנס קישור לסרטון יוטיוב: ")
    download_video(url)
    upload_to_drive()

if __name__ == "__main__":
    main()