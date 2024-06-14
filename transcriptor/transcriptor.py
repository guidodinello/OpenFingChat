"""
  1. For each lecture document in MONGODB
    1.1 Download lectue video in MP4 format
    1.2 Convert lecture to MP3 format
    1.3 Transcribe lecture using Whisper
    1.4 Save transcription
    1.5 Delete MP4 and MP3 files
"""

from pymongo import MongoClient
from moviepy.editor import VideoFileClip
import requests
import os
from tqdm import tqdm
from whisper
import json

BASE_PATH = '../store/transcriptions/'

def convert_video_to_audio(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)
    audio = video.audio
    audio.write_audiofile(audio_file_path)
    audio.close()
    video.close()

def download_video(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(file_path, 'wb') as file, tqdm(
                desc=file_path,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
        print(f"Download completed: {file_path}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")



def transcribe_audio_with_timestamps(audio_file_path, transcription_file_path, change_timestamps=False, start_offset=0, end_offset=0):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    segments = []

    for segment in result['segments']:
        start_time = segment['start'] + start_offset if change_timestamps else segment['start']
        end_time = segment['end'] + end_offset if change_timestamps else segment['end']

        segments.append({
            "text": segment['text'],
            "start": start_time,
            "end": end_time
            })

    with open(transcription_file_path, 'w') as f:
        json.dump(segments, f, ensure_ascii=False, indent=4)

    return segments



uri='mongodb+srv://spoturno:AJFY2oSTelEuFT66@webirdatabase.slyw0m4.mongodb.net/?retryWrites=true&w=majority&appName=WebirDatabase'
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=False)
db = client['webir']
collection = db['lessons']

all_documents = collection.find()
documents_list = list(all_documents)

os.makedirs(BASE_PATH, exist_ok=True)

for document in documents_list[:1]:
    video_file_path = os.path.join(BASE_PATH, f'{document["_id"]}.mp4')
    audio_file_path = os.path.join(BASE_PATH, f'{document["_id"]}.mp3')
    transcription_file_path = os.path.join(BASE_PATH, f'{document["_id"]}.json')

    download_video(document['video'], video_file_path)
    convert_video_to_audio(video_file_path, audio_file_path)
    transcribe_audio_with_timestamps(audio_file_path, transcription_file_path, False, 0, 0)

    os.remove(video_file_path)
    os.remove(audio_file_path)

