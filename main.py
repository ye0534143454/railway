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
    media_type = os.environ.get("MEDIA_TYPE", "audio")

    if media_type == "video":
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get("title", "video"))
            filename = f"{title}.mp4"

        options = {
            'outtmpl': filename,
            'format': 'worst[ext=mp4]/worst',
            'quiet': True
        }
    else:
        options_probe = {
            'quiet': True,
            'skip_download': True
        }
        with yt_dlp.YoutubeDL(options_probe) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get("title", "audio"))
            formats = info.get("formats", [])
            best_audio = next((f for f in formats if f.get("vcodec") == "none"), {})
            ext = best_audio.get("ext", "m4a")
            filename = f"{title}.{ext}"

        options = {
            'outtmpl': filename,
            'format': 'bestaudio/worst',
            'quiet': True,
            'postprocessors': []
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    upload_to_drive(filename, filename, drive)

def download_channel(channel_url, drive):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'playliststart': 1
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', [])
        print(f"Found {len(entries)} videos in channel")

        for entry in entries:
            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
            download_video(video_url, drive)

def main():
    video_url = os.environ.get("VIDEO_URL")
    collection_url = os.environ.get("COLLECTION_URL")

    if video_url:
        drive = get_drive()
        download_video(video_url, drive)
    elif collection_url:
        drive = get_drive()
        download_channel(collection_url, drive)
    else:
        raise ValueError("Either VIDEO_URL or CHANNEL_URL must be defined")

if __name__ == "__main__":
    main()
