from __future__ import annotations

import argparse
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise EnvironmentError(f"Required environment variable is missing: {name}")
    return value


def _build_credentials() -> Credentials:
    credentials = Credentials(
        token=None,
        refresh_token=_required_env("YT_REFRESH_TOKEN"),
        token_uri=TOKEN_URI,
        client_id=_required_env("YT_CLIENT_ID"),
        client_secret=_required_env("YT_CLIENT_SECRET"),
        scopes=[YOUTUBE_UPLOAD_SCOPE],
    )
    credentials.refresh(Request())
    return credentials


def upload_video(
    file_path: Path,
    title: str,
    description: str,
    publish: bool,
    category_id: str,
    tags: list[str],
) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Video file not found: {file_path}")

    youtube = build("youtube", "v3", credentials=_build_credentials())

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": "public" if publish else "private",
                "selfDeclaredMadeForKids": True,
            },
        },
        media_body=MediaFileUpload(str(file_path), chunksize=-1, resumable=True),
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    return response["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload rendered video to YouTube.")
    parser.add_argument("--file", required=True, help="Path to MP4 file.")
    parser.add_argument("--title", required=True, help="Video title.")
    parser.add_argument("--description", default="", help="Video description.")
    parser.add_argument("--publish", default="true", choices=["true", "false"], help="Publish immediately.")
    parser.add_argument("--category", default="24", help="YouTube category id.")
    parser.add_argument("--tags", nargs="*", default=["cartoon", "kids", "animation"], help="Video tags.")
    args = parser.parse_args()

    video_id = upload_video(
        file_path=Path(args.file),
        title=args.title,
        description=args.description,
        publish=args.publish == "true",
        category_id=args.category,
        tags=args.tags,
    )
    print(f"Uploaded video id: {video_id}")


if __name__ == "__main__":
    main()
