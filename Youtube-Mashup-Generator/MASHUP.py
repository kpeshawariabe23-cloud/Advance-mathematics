import sys
import os
import shutil

def validate_args(args):
    if len(args) != 4:
        print("Error: Incorrect number of arguments.")
        print("Usage : python RollNumber.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        print('Example: python RollNumber.py "Sharry Maan" 20 25 output.mp3')
        sys.exit(1)

    singer_name, num_videos_str, audio_duration_str, output_file = args

    # NumberOfVideos must be > 10
    try:
        num_videos = int(num_videos_str)
        if num_videos <= 10:
            raise ValueError
    except ValueError:
        print(f"Error: <NumberOfVideos> must be an integer greater than 10. Got: '{num_videos_str}'")
        sys.exit(1)

    # AudioDuration must be > 20
    try:
        audio_duration = int(audio_duration_str)
        if audio_duration <= 20:
            raise ValueError
    except ValueError:
        print(f"Error: <AudioDuration> must be an integer greater than 20. Got: '{audio_duration_str}'")
        sys.exit(1)

    # Output file must end with .mp3
    if not output_file.endswith(".mp3"):
        print(f"Error: <OutputFileName> must end with '.mp3'. Got: '{output_file}'")
        sys.exit(1)

    return singer_name, num_videos, audio_duration, output_file



def download_videos(singer_name, num_videos, download_dir):
    try:
        import yt_dlp
    except ImportError:
        print("'yt-dlp' not found. Install it: pip install yt-dlp")
        sys.exit(1)

    print(f"\nSearching YouTube for '{singer_name}' ({num_videos} videos)...")
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": os.path.join(VID_DIR, "%(autonumber)s_%(title)s.%(ext)s"),
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
        print("No videos downloaded. Check internet/singer name.")
        sys.exit(1)

    print(f"Downloaded {len(downloaded)} video(s).")
    return downloaded


def convert_to_audio(video_files, audio_dir):
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        print("'moviepy' not found. Install it: pip install moviepy")
        sys.exit(1)

    os.makedirs(audio_dir, exist_ok=True)
    audio_files = []

    print("\nConverting videos to audio...")
    for i, vpath in enumerate(video_files, 1):
        try:
            base = os.path.splitext(os.path.basename(vpath))[0]
            apath = os.path.join(audio_dir, f"{base}.mp3")
            print(f"  [{i}/{len(video_files)}] {os.path.basename(vpath)}")

            with VideoFileClip(vpath) as clip:
                if clip.audio is None:
                    print("  Warning: No audio track. Skipping.")
                    continue
                clip.audio.write_audiofile(apath, logger=None)

            audio_files.append(apath)
        except Exception as e:
            print(f"  Warning: Skipping '{os.path.basename(vpath)}' – {e}")

    if not audio_files:
        print("No audio files created.")
        sys.exit(1)

    print(f"Converted {len(audio_files)} file(s).")
    return audio_files


def cut_clips(audio_files, duration_sec, clip_dir):
    try:
        from pydub import AudioSegment
    except ImportError:
        print("'pydub' not found. Install it: pip install pydub")
        sys.exit(1)

    os.makedirs(clip_dir, exist_ok=True)
    clipped = []
    ms = duration_sec * 1000

    print(f"\nCutting first {duration_sec}s from each audio...")
    for i, apath in enumerate(audio_files, 1):
        try:
            bname = os.path.basename(apath)
            cpath = os.path.join(clip_dir, f"clip_{bname}")
            print(f"  [{i}/{len(audio_files)}] {bname}")

            seg = AudioSegment.from_mp3(apath)
            chunk = seg[:ms] if len(seg) >= ms else seg
            chunk.export(cpath, format="mp3")
            clipped.append(cpath)
        except Exception as e:
            print(f"  Warning: Skipping '{os.path.basename(apath)}' – {e}")

    if not clipped:
        print("No clipped files created.")
        sys.exit(1)

    print(f"Clipped {len(clipped)} file(s).")
    return clipped


def merge_clips(clipped_files, output_file):
    try:
        from pydub import AudioSegment
    except ImportError:
        print("'pydub' not found. Install it: pip install pydub")
        sys.exit(1)

    print(f"\nMerging {len(clipped_files)} clips → '{output_file}'...")
    combined = AudioSegment.empty()

    for i, cpath in enumerate(clipped_files, 1):
        try:
            print(f"  [{i}/{len(clipped_files)}] {os.path.basename(cpath)}")
            combined += AudioSegment.from_mp3(cpath)
        except Exception as e:
            print(f"  Warning: Skipping '{os.path.basename(cpath)}' – {e}")

    if len(combined) == 0:
        print("Merged audio is empty.")
        sys.exit(1)

    combined.export(output_file, format="mp3")
    print(f"\nDone! Mashup saved as '{output_file}'")
    print(f"Total duration: {len(combined)/1000:.1f} seconds")


def main():
    singer, n_videos, duration, out_file = validate_args(sys.argv[1:])

    print("=" * 50)
    print("  YouTube Mashup Creator")
    print("=" * 50)
    print(f"  Singer        : {singer}")
    print(f"  Videos        : {n_videos}")
    print(f"  Clip duration : {duration}s")
    print(f"  Output file   : {out_file}")
    print("=" * 50)

    VID_DIR  = "temp_videos"
    AUD_DIR  = "temp_audio"
    CLIP_DIR = "temp_clips"

    try:
        videos  = download_videos(singer, n_videos, VID_DIR)
        audios  = convert_to_audio(videos, AUD_DIR)
        clips   = cut_clips(audios, duration, CLIP_DIR)
        merge_clips(clips, out_file)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
    finally:

        for d in (VID_DIR, AUD_DIR, CLIP_DIR):
            if os.path.exists(d):
                shutil.rmtree(d)
        print("Temp files removed.")


if __name__ == "__main__":
    main()