"""
  1. For each lecture document in MONGODB
    1.1 Download lectue video in MP4 format
    1.2 Convert lecture to MP3 format
    1.3 Transcribe lecture using Whisper
    1.4 Save transcription
    1.5 Delete MP4 and MP3 files
"""

from moviepy.editor import VideoFileClip
import requests
import os
from tqdm import tqdm
import whisper
import json
from store.data.models.lessons import LessonModel
from bson import ObjectId
import os
import logging


BASE_PATH = 'store/transcriptions/'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_video_to_audio(video_file_path, audio_file_path):
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(audio_file_path)
        audio.close()
        video.close()
        logging.info(f"Audio extracted and saved to: {audio_file_path}")
    except Exception as e:
        logging.error(f"Error converting video to audio: {e}")
        raise

def download_video(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
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
        logging.info(f"Download completed: {file_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download video: {e}")
        raise


def transcribe_audio_with_whisper(audio_file_path, transcription_file_path, change_timestamps=False, start_offset=0, end_offset=0):
    try:
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

        logging.info(f"Transcription saved to: {transcription_file_path}")
        return segments
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        raise


def transcript():

    # Esto podría ser una variable de entorno o un argumento
    subject_ids = [
        '66567efb97cf1d12f025fde5', # AGPI
        '66567f1097cf1d12f025fe07', # Algoritmos Evolutivos
        '66567f8197cf1d12f025feb7', # Aplicaciones del Algebra Lineal
        '665681ca97cf1d12f026025f', # Economía
        '6656821b97cf1d12f02602e3', # El Negocio del Software,
        '665683dc97cf1d12f02605c5', # Física 1
        '665684ff97cf1d12f02607a3', # GAL 1
    ]

    lesson_model = LessonModel()    

    os.makedirs(BASE_PATH, exist_ok=True)

    for subject_id in subject_ids:
        filters = {"subjectId": ObjectId(subject_id), "transcribed": False}
        lessons = lesson_model.getAll(**filters)
        for lesson in lessons:
            video_file_path = os.path.join(BASE_PATH, f"{lesson['_id']}.mp4")
            audio_file_path = os.path.join(BASE_PATH, f"{lesson['_id']}.mp3")
            transcription_file_path = os.path.join(BASE_PATH, f"{lesson['_id']}.json")
            try:
                download_video(lesson['video'], video_file_path)
                convert_video_to_audio(video_file_path, audio_file_path)
                transcribe_audio_with_whisper(audio_file_path, transcription_file_path)
                lesson_model.update(lesson['_id'], {"transcribed": True})
            except Exception as e:
                logging.error(f"Failed to process lesson {lesson['_id']}: {e}")
            finally:
                if os.path.exists(video_file_path):
                    os.remove(video_file_path)
                if os.path.exists(audio_file_path):
                    os.remove(audio_file_path)