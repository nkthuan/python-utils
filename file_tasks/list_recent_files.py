"""
Description:
Recursively list all files with specified extension and created within a time frame inside specified directory.

Author: nkthuan
"""

import argparse
import os
from datetime import datetime, timedelta
import sys

LINE_PREFIX = "\t"
DEFAULT_DAYS_THRESHOLD = 500
DEFAULT_FILE_TYPE = "pdf"

formatted_result = []


def list_recent_files(directory, extension, days_threshold):
    cur_files = []
    count = 0

    for entry in os.scandir(directory):
        if entry.is_dir():
            # recursive call for this subdirectory
            count += list_recent_files(entry.path, extension, days_threshold)
        elif (
            entry.is_file()
            and entry.name.lower().endswith(extension)
            and created_within_days(entry, days_threshold)
        ):
            cur_files.append(entry.name)

    if cur_files:
        formatted_result.append(directory)
        formatted_result.extend(f"{LINE_PREFIX}{file}" for file in cur_files)
        count += len(cur_files)

    return count


def created_within_days(fileEntry, days):
    file_creation_time = datetime.fromtimestamp(fileEntry.stat().st_ctime)
    threshold_date = datetime.now() - timedelta(days=days)
    return file_creation_time >= threshold_date


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description="Recursively list all files with specified extension and created within a time frame inside specified directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "inputDirectory",
        help="Path of the directory to list recent files (all subdirectories considered).",
    )
    parser.add_argument(
        "--filetype", help="File type to list.", default=DEFAULT_FILE_TYPE
    )
    parser.add_argument(
        "--days",
        help="Number of days to look back.",
        type=int,
        default=DEFAULT_DAYS_THRESHOLD,
    )

    return parser.parse_args()


def get_extension(args):
    file_type = args.filetype
    # This seems too much to me but let's be lenient about the input
    if "." in file_type:
        file_type = file_type[1:]

    # normalize, because user can enter something like doC
    return ("." + file_type).lower()


def get_days_threshold(args):
    days_threshold = args.days if args.days > 0 else DEFAULT_DAYS_THRESHOLD
    return days_threshold


if __name__ == "__main__":
    args = get_parsed_args()

    inputDirectory = args.inputDirectory
    if not os.path.exists(inputDirectory) or not os.path.isdir(inputDirectory):
        print("Invalid directory path.")
        sys.exit()

    extension = get_extension(args)

    days_threshold = get_days_threshold(args)

    count = list_recent_files(
        os.path.normpath(inputDirectory), extension, days_threshold
    )
    print(
        f"Listing all {count} {extension[1:].upper()} files created in the last {days_threshold} days:"
    )
    for line in formatted_result:
        print(line)
