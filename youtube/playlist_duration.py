"""
Description:
Calculate total duration of videos in a YouTube playlist.

Author: nkthuan
"""

import argparse
import os
from dotenv import load_dotenv

from .youtube_utils import (
    calculate_total_duration,
    fetch_all_playlist_videos,
    fetch_video_durations_in_bulk,
)

load_dotenv()


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description="Calculate total duration of videos in a YouTube playlist.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "playlistId",
        help="YouTube playlist ID (the part after /playlist?list= in the URL).",
    )

    return parser.parse_args()


def main_process(playlist_id, api_key):
    print("=== Fetching videos from playlist...")
    videos = fetch_all_playlist_videos(playlist_id, api_key)

    video_ids = [video["snippet"]["resourceId"]["videoId"] for video in videos]

    print("\n=== Fetching video durations in bulk...")
    video_durations = fetch_video_durations_in_bulk(video_ids, api_key)

    total_duration = calculate_total_duration(video_durations)
    print(f"\nTotal duration of playlist: {total_duration}")


if __name__ == "__main__":
    args = get_parsed_args()

    playlist_id = args.playlistId

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Make sure to set YOUTUBE_API_KEY in your .env file."
        )

    main_process(playlist_id, api_key)
