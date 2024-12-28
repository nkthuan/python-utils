# <h1 align="center">Python Utilities</h1>

A collection of Python utility scripts.

## Installation

To set up the project on your local machine, follow these steps:

### Step 1: (Optional) Create a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 2: Install Dependencies

Make sure you have Python installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Instructions on the usage of the scripts:

- Generally, just run each script with the option -h to learn about it.
- Rename the file .env.sample to .env and put any necessary environment variables there.
- Be careful about API quota usage.

### Calculate videos duration

Calculate the total duration of videos inside a specified directory (and its subdirectories).

```bash
python calculate_videos_duration.py -h
```

### List recent files

Recursively list all files with specified extension and created within a time frame inside specified directory.

### YouTube playlist duration

Calculate total duration of videos in a YouTube playlist.

## License

This project is licensed under the [Apache License 2.0](LICENSE). You are free to use, modify, and distribute this software under the terms of the license.

## Contact

For questions or issues, feel free to open an issue in this repository or contact me via email.
