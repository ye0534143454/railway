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
    url = "https://www.youtube.com/results?search_query=%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20kerbal%20space%20program%20%D7%91%D7%A2%D7%91%D7%A8%D7%99%D7%AA%20%D7%A4%D7%A8%D7%A7%20%D7%A8%D7%90%D7%A9%D7%95%D7%9F&sp=EgIQAQ%253D%253D")
    download_video(url)
    upload_to_drive()

if __name__ == "__main__":
    main()