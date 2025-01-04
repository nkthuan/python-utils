from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate  # For parsing ISO 8601 durations


def sanitized_error_messasge(error, api_key):
    """
    Redacts sensitive information (e.g., API keys) from Google API HttpError messages.
    """
    try:
        error_message = str(error)

        # If developer provided an invalid api key, it's ok to show it back to him (it's useless anyway)
        if "api key not valid" in error_message.lower():
            return f"Error:\n{error_message}"

        error_message = error_message.replace("\n", " ")
        sanitized_message = error_message.replace(api_key, "[REDACTED]")

        return f"Error (sanitized):\n{sanitized_message}"
    except Exception as e:
        print(f"Could not process error message. Exception: {str(e)}")
        return str(error)


def fetch_all_playlist_videos(playlist_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    all_videos = []

    try:
        # Initial request to fetch the first page of results
        request = youtube.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50
        )
        while request:
            response = request.execute()

            all_videos.extend(response.get("items", []))

            # Get the next page of results
            request = youtube.playlistItems().list_next(request, response)
    except HttpError as e:
        print(sanitized_error_messasge(e, api_key))

    print(f"Total videos retrieved: {len(all_videos)}")
    return all_videos


def fetch_video_durations_in_bulk(video_ids, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    durations = {}

    # Process in batches of 50 video IDs
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i : i + 50]

        try:
            response = (
                youtube.videos()
                .list(part="contentDetails", id=",".join(batch_ids))
                .execute()
            )

            for item in response.get("items", []):
                video_id = item["id"]
                iso_duration = item["contentDetails"]["duration"]
                durations[video_id] = isodate.parse_duration(
                    iso_duration
                ).total_seconds()

        except HttpError as e:
            print(sanitized_error_messasge(e, api_key))

    return durations


def calculate_total_duration(durations):
    total_duration_seconds = sum(durations.values())

    hours, remainder = divmod(int(total_duration_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    result = f"{hours:02}:{minutes:02}:{seconds:02}"

    if hours > 24:
        days, hours = divmod(hours, 24)
        result += f"\nOR\n{days:02}:{hours:02}:{minutes:02}:{seconds:02}"

    return result
