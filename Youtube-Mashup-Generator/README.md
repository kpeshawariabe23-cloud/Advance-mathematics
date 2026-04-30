## Project Description
This project performs song mashup generation using audio processing techniques.

## What's Inside

**Program 1** - Command line script that does the heavy lifting  
**Program 2** - Flask web app with a form and email delivery

## Setup

### Install Dependencies
```bash
pip install yt-dlp moviepy==1.0.3 pydub flask
```

You'll also need:
- **Node.js** - Download from nodejs.org
- **FFmpeg** - Google "install ffmpeg [your OS]" for instructions

### YouTube Cookies (Important!)

YouTube blocks bots, so you need to give the script your login cookies:

1. Install the browser extension **"Get cookies.txt LOCALLY"**
2. Go to youtube.com (make sure you're logged in)
3. Click the extension and export as `cookies.txt`
4. Put `cookies.txt` in this folder

### Email Setup (for web app)

Open `app.py` and change these lines:
```python
SENDER_EMAIL        = "your_email@gmail.com"
SENDER_APP_PASSWORD = "your_app_password_here"
```

For Gmail, you need an App Password (not your regular password):
- Go to Google Account â†’ Security â†’ 2-Step Verification (turn it on)
- Search "App Passwords" â†’ Generate one for Mail
- Copy the 16-character password

## Usage

### Command Line

```bash
python RollNumber.py "Arijit Singh" 15 30 output.mp3
```

This downloads 15 Arijit Singh videos, cuts the first 30 seconds from each, and merges them.

Rules:
- Number of videos must be > 10
- Duration must be > 20 seconds
- Output filename must end with `.mp3`

### Web App

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. Fill out the form and the mashup gets emailed to you as a zip file.

## How It Works

1. **Download** - Uses yt-dlp to search and download YouTube videos
2. **Convert** - MoviePy extracts audio from videos
3. **Trim** - PyDub cuts the first N seconds from each audio file
4. **Merge** - Combines all clips into one MP3
5. **Email** (web app only) - Zips the file and sends it via SMTP

## Submitted By
Keshav Peshawaria


