from flask import Flask, render_template, request
import os, shutil, zipfile, smtplib, ssl
from email.message import EmailMessage

app = Flask(__name__)

SENDER_EMAIL = "keshavbansal937@gmail.com"
SENDER_APP_PASSWORD = "nuphgchnoppepjai"  # Gmail App Password


SMTP_PROVIDERS = {
    "gmail.com":      {"host": "smtp.gmail.com",      "port": 587},
    "yahoo.com":      {"host": "smtp.mail.yahoo.com", "port": 587},
    "yahoo.in":       {"host": "smtp.mail.yahoo.com", "port": 587},
    "outlook.com":    {"host": "smtp.office365.com",  "port": 587},
    "hotmail.com":    {"host": "smtp.office365.com",  "port": 587},
    "live.com":       {"host": "smtp.office365.com",  "port": 587},
    "icloud.com":     {"host": "smtp.mail.me.com",    "port": 587},
    "zoho.com":       {"host": "smtp.zoho.com",       "port": 587},
    "protonmail.com": {"host": "smtp.protonmail.com", "port": 587},
}

def get_smtp_settings(email):
    domain = email.split("@")[-1].lower()
    if domain in SMTP_PROVIDERS:
        return SMTP_PROVIDERS[domain]
    return {"host": f"smtp.{domain}", "port": 587}



def send_email(recipient_email, subject, body, attachment_path):
    smtp_settings = get_smtp_settings(SENDER_EMAIL)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = recipient_email
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename="mashup.zip"
        )

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_settings["host"], smtp_settings["port"]) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.send_message(msg)



def download_videos(singer_name, num_videos, download_dir):
    try:
        import yt_dlp
    except ImportError:
        raise Exception("'yt-dlp' not found. Run: pip install yt-dlp")

    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": os.path.join(download_dir, "%(autonumber)s_%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "merge_output_format": "mp4",
        "cookiefile": "cookies.txt",
        "js_runtimes": {"node": {}},
        "remote_components": "ejs:github",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer_name} song"])

    downloaded = [
        os.path.join(download_dir, f)
        for f in sorted(os.listdir(download_dir))
        if f.lower().endswith((".mp4", ".webm", ".mkv"))
    ]

    if not downloaded:
        raise Exception("No videos downloaded. Check your internet or singer name.")

    return downloaded



def convert_to_audio(video_files, audio_dir):
    try:
        from moviepy import VideoFileClip
    except ImportError:
        raise Exception("'moviepy' not found. Run: pip install moviepy==1.0.3")

    os.makedirs(audio_dir, exist_ok=True)
    audio_files = []

    for vpath in video_files:
        try:
            base  = os.path.splitext(os.path.basename(vpath))[0]
            apath = os.path.join(audio_dir, f"{base}.mp3")
            with VideoFileClip(vpath) as clip:
                if clip.audio:
                    clip.audio.write_audiofile(apath, logger=None)
                    audio_files.append(apath)
        except Exception:
            continue

    if not audio_files:
        raise Exception("No audio files created after conversion.")

    return audio_files


def cut_clips(audio_files, duration_sec, clip_dir):
    try:
        from pydub import AudioSegment
    except ImportError:
        raise Exception("'pydub' not found. Run: pip install pydub")

    os.makedirs(clip_dir, exist_ok=True)
    clipped_files = []
    duration_ms = duration_sec * 1000

    for apath in audio_files:
        try:
            cpath = os.path.join(clip_dir, f"clip_{os.path.basename(apath)}")
            seg   = AudioSegment.from_mp3(apath)
            chunk = seg[:duration_ms] if len(seg) >= duration_ms else seg
            chunk.export(cpath, format="mp3")
            clipped_files.append(cpath)
        except Exception:
            continue

    if not clipped_files:
        raise Exception("No clipped files created.")

    return clipped_files


def merge_clips(clipped_files, output_file):
    try:
        from pydub import AudioSegment
    except ImportError:
        raise Exception("'pydub' not found. Run: pip install pydub")

    combined = AudioSegment.empty()
    for cpath in clipped_files:
        try:
            combined += AudioSegment.from_mp3(cpath)
        except Exception:
            continue

    if len(combined) == 0:
        raise Exception("Merged audio is empty.")

    combined.export(output_file, format="mp3")


def run_mashup(singer_name, num_videos, duration, output_file):
    VID_DIR  = "temp_videos"
    AUD_DIR  = "temp_audio"
    CLIP_DIR = "temp_clips"

    try:
        videos  = download_videos(singer_name, num_videos, VID_DIR)
        audios  = convert_to_audio(videos, AUD_DIR)
        clips   = cut_clips(audios, duration, CLIP_DIR)
        merge_clips(clips, output_file)
    finally:
        for d in (VID_DIR, AUD_DIR, CLIP_DIR):
            if os.path.exists(d):
                shutil.rmtree(d)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer          = request.form.get("singer_name", "").strip()
        n               = request.form.get("num_videos", "")
        duration        = request.form.get("duration", "")
        recipient_email = request.form.get("email", "").strip()

        # Validation
        errors = []
        if not singer:
            errors.append("Singer name is required.")
        try:
            n = int(n)
            if n <= 10:
                errors.append("Number of videos must be greater than 10.")
        except ValueError:
            errors.append("Number of videos must be a valid integer.")
        try:
            duration = int(duration)
            if duration <= 20:
                errors.append("Duration must be greater than 20 seconds.")
        except ValueError:
            errors.append("Duration must be a valid integer.")
        if not recipient_email or "@" not in recipient_email:
            errors.append("Enter a valid email address.")

        if errors:
            return render_template("index.html", errors=errors)

        try:
            output_mp3 = "output.mp3"
            output_zip = "output.zip"

            run_mashup(singer, n, duration, output_mp3)

            with zipfile.ZipFile(output_zip, "w") as zf:
                zf.write(output_mp3, arcname="mashup.mp3")

            send_email(
                recipient_email=recipient_email,
                subject=f"Your {singer} Mashup!",
                body=f"Hi,\n\nYour mashup of {n} {singer} songs ({duration}s each) is attached!\n\nEnjoy!",
                attachment_path=output_zip
            )

            if os.path.exists(output_mp3):
                os.remove(output_mp3)
            if os.path.exists(output_zip):
                os.remove(output_zip)

            return render_template("index.html", success=f"Mashup sent successfully to {recipient_email}!")

        except smtplib.SMTPAuthenticationError:
            return render_template("index.html", error="Email authentication failed. Check your App Password.")
        except smtplib.SMTPException as e:
            return render_template("index.html", error=f"Email error: {str(e)}")
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)