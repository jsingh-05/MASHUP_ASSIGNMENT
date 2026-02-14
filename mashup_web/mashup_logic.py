import os
import shutil
import zipfile
import yt_dlp
from pydub import AudioSegment


BASE_DIR = "processing"
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
SEGMENT_DIR = os.path.join(BASE_DIR, "segments")


def reset_workspace():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(DOWNLOAD_DIR)
    os.makedirs(AUDIO_DIR)
    os.makedirs(SEGMENT_DIR)


def build_audio_mashup(artist_name, video_count, clip_length):
    search_query = f"ytsearch{video_count}:{artist_name}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    for file in os.listdir(DOWNLOAD_DIR):
        input_path = os.path.join(DOWNLOAD_DIR, file)
        audio = AudioSegment.from_file(input_path)
        audio.export(os.path.join(AUDIO_DIR, f"{file}.mp3"), format="mp3")

    combined = AudioSegment.empty()

    for file in os.listdir(AUDIO_DIR):
        audio = AudioSegment.from_mp3(os.path.join(AUDIO_DIR, file))
        trimmed = audio[:clip_length * 1000]
        combined += trimmed

    output_path = os.path.join(BASE_DIR, "mashup.mp3")
    combined.export(output_path, format="mp3")

    return output_path


def package_output(mashup_path):
    zip_path = os.path.join(BASE_DIR, "mashup_package.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(mashup_path, arcname="mashup.mp3")
    return zip_path
