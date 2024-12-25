import argparse
import os
import sys
from pymediainfo import MediaInfo


VIDEO_EXTENSIONS = (
    ".mp4",
    ".mkv",
    ".m4v",
    ".avi",
    ".mov",
    ".flv",
    ".wmv",
    ".3gp",
    ".webm",
)


def get_video_duration(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == "Video":
            return float(track.duration) / (1000 * 60)
    raise Exception("Sorry, video track not found in this file.")


def calculate_total_duration(directory_path):
    total_duration = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(VIDEO_EXTENSIONS):
                file_path = os.path.join(root, file)
                total_duration += get_video_duration(file_path)

    return total_duration


def convert_to_hours_minutes(total_minutes):
    hours, minutes = divmod(total_minutes, 60)
    return f"{int(hours)}h {minutes:.2f}m"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputDirectory",
        help="Path of the directory to calculate total videos duration.",
    )
    args = parser.parse_args()
    if not os.path.exists(args.inputDirectory):
        print("Invalid directory path. Failed to calculate.")
        sys.exit()

    total_duration = calculate_total_duration(args.inputDirectory)
    print(
        f"The total duration is: {total_duration:.2f} minutes, or {convert_to_hours_minutes(total_duration)}"
    )
