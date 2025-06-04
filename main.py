import json
import os
import yt_dlp
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import re

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '_', title)

def get_drive():
    credentials_json_str = os.environ.get('CREDENTIALS_JSON')
    if not credentials_json_str:
        raise ValueError("Environment variable CREDENTIALS_JSON is not defined")

    with open("credentials.json", "w") as f:
        json.dump(json.loads(credentials_json_str), f)

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        raise RuntimeError("Invalid credentials.json")
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    os.remove("credentials.json")
    return GoogleDrive(gauth)

def upload_to_drive(filepath, filename, drive):
    f = drive.CreateFile({'title': filename})
    f.SetContentFile(filepath)
    f.Upload()
    print(f"Uploaded: {filename}")
    os.remove(filepath)

def download_video(url, drive):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get("title", "video"))
        filename = f"{title}.mp4"

    options = {
        'outtmpl': filename,
        'format': 'worst[ext=mp4]/worst',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    upload_to_drive(filename, filename, drive)

def download_channel(channel_url, drive):
    print (channel_url)
    start_index = int(os.environ.get("PLAYLIST_START", 1))
    end_index = os.environ.get("PLAYLIST_END")
    if end_index:
        end_index = int(end_index)

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playliststart': start_index
    }
    if end_index:
        ydl_opts['playlistend'] = end_index

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', [])
        print(f"Found {len(entries)} videos in collection")

        for entry in entries:
            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
            download_video(video_url, drive)


def main():
    video_url = os.environ.get("VIDEO_URL")
    channel_url = os.environ.get("CHANNEL_URL")
    print("VIDEO_URL:", video_url)
    print("CHANNEL_URL:", channel_url)

    if video_url:
        drive = get_drive()
        download_video(video_url, drive)
    elif channel_url:
        drive = get_drive()
        download_channel(channel_url, drive)
    else:
        raise ValueError("Either VIDEO_URL or CHANNEL_URL must be defined")

if __name__ == "__main__":
    main()
