import json
import os
import pickle
import sys
from datetime import datetime

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = "token.pkl"
VIDEO_PATH = "final_output.mp4"


def get_authenticated_service():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"{TOKEN_PATH} not found.")
    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        print("Token expired — refreshing...")
        creds.refresh(Request())
        with open(TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, file_path: str):
    date_str = datetime.now().strftime("%B %d, %Y")
    title = f"South Africans Being South Africans 😂 | Funny SA Moments {date_str}"[:100]

    description = (
        "The funniest South African moments you'll see today! "
        "Only in Mzansi 🇿🇦😂\n\n"
        "#SouthAfrica #Mzansi #SouthAfricanLiving #FunnySA #SAMoments "
        "#OnlyInSouthAfrica #SouthAfricanHumor #Amapiano #MzansiFunny "
        "#SouthAfricanTikTok #Viral #Funny #Comedy"
    )

    tags = [
        "South Africa", "Mzansi", "funny south africa", "south african living",
        "only in south africa", "sa moments", "south african humor",
        "mzansi funny", "south african tiktok", "funny", "comedy", "viral"
    ]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "23",  # Comedy
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True, chunksize=8 * 1024 * 1024)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"\nUploading: {file_path}")
    print(f"  Title: {title}")

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Progress: {int(status.progress() * 100)}%")

    video_id = response.get("id", "unknown")
    print(f"  Done: https://www.youtube.com/watch?v={video_id}")
    return video_id


def main():
    if not os.path.exists(VIDEO_PATH):
        print(f"No video found at {VIDEO_PATH}")
        sys.exit(1)

    youtube = get_authenticated_service()

    try:
        vid_id = upload_video(youtube, VIDEO_PATH)
        print(f"\nUploaded successfully: {vid_id}")
    except Exception as e:
        print(f"Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
