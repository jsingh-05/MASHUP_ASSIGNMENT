import os
import sys
import shutil
import yt_dlp
from pydub import AudioSegment


DOWNLOAD_DIR = "downloads"
AUDIO_DIR = "audio_tracks"
SEGMENT_DIR = "segments"


def validate_inputs(video_count, clip_length):
    if video_count <= 10:
        raise ValueError("Video count must be greater than 10.")
    if clip_length <= 20:
        raise ValueError("Clip duration must be greater than 20 seconds.")


def prepare_directories():
    for folder in [DOWNLOAD_DIR, AUDIO_DIR, SEGMENT_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)


def download_videos(artist_name, video_count):
    search_query = f"ytsearch{video_count}:{artist_name}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])


def convert_to_audio():
    for file in os.listdir(DOWNLOAD_DIR):
        input_path = os.path.join(DOWNLOAD_DIR, file)
        audio = AudioSegment.from_file(input_path)
        output_path = os.path.join(AUDIO_DIR, f"{file}.mp3")
        audio.export(output_path, format="mp3")


def trim_audio_segments(clip_length):
    for file in os.listdir(AUDIO_DIR):
        path = os.path.join(AUDIO_DIR, file)
        audio = AudioSegment.from_mp3(path)
        trimmed = audio[:clip_length * 1000]
        trimmed.export(os.path.join(SEGMENT_DIR, file), format="mp3")


def merge_segments(output_file):
    combined = AudioSegment.empty()

    for file in os.listdir(SEGMENT_DIR):
        path = os.path.join(SEGMENT_DIR, file)
        segment = AudioSegment.from_mp3(path)
        combined += segment

    combined.export(output_file, format="mp3")


def main():
    if len(sys.argv) != 5:
        print("Usage: python audio_mashup_cli.py <ArtistName> <VideoCount> <ClipLength> <OutputFile>")
        sys.exit(1)

    artist_name = sys.argv[1]
    video_count = int(sys.argv[2])
    clip_length = int(sys.argv[3])
    output_file = sys.argv[4]

    try:
        validate_inputs(video_count, clip_length)
        prepare_directories()
        download_videos(artist_name, video_count)
        convert_to_audio()
        trim_audio_segments(clip_length)
        merge_segments(output_file)
        print("Mashup created successfully.")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
