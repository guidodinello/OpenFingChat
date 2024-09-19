import logging
import os
from typing import List, Optional, Union

import requests
import whisper
from tqdm import tqdm

import constants
from store.mongo.models.lessons import LessonModel
from transcriptor import steps


def download_video(url: str, file_path: os.PathLike) -> Optional[bool]:
    try:
        # TODO: use a faster download method.
        # https://stackoverflow.com/questions/71872663/speed-up-python-requests-download-speed-by-behaving-appropriately-around-thrott
        response = requests.get(url, stream=True, timeout=None)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        with open(file_path, "wb") as file, tqdm(
            desc=str(file_path),
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
        logging.info("Download completed:  %s", file_path)
        return True
    except requests.exceptions.RequestException as e:
        logging.error("Failed to download video:  %s", e)
        return None


def transcript(
    config: dict, subject_names: List[str], max_lessons: Union[int | None] = None
) -> None:
    constants.BASE_PATH.mkdir(parents=True, exist_ok=True)
    lessons = steps.untranscribed_lessons(subject_names, max_lessons)
    lesson_model = LessonModel()

    model = whisper.load_model(
        config["MODEL"],
        device=config["DEVICE"],
        download_root=config["CACHE_PATH"],
        in_memory=True,
    )

    for lesson in lessons:
        video_file_path = constants.BASE_PATH / f"{lesson["lesson_id"]}.mp4"
        audio_file_path = constants.BASE_PATH / f"{lesson["lesson_id"]}.mp3"
        transcription_file_path = constants.BASE_PATH / f"{lesson["lesson_id"]}.json"

        if transcription_file_path.exists():
            logging.warning(
                "Lesson %s is marked as not transcribed but transcription file exists. Skipping lesson...",
                lesson["lesson_id"],
            )
            continue

        if not video_file_path.exists() and not audio_file_path.exists():
            success = download_video(lesson["video"], video_file_path)
            if success is None:
                video_file_path.unlink(missing_ok=True)  # dont want corrupted files
        if not audio_file_path.exists():
            success = steps.convert_video_to_audio(video_file_path, audio_file_path)
            if success is None:
                audio_file_path.unlink(missing_ok=True)

        transcription = steps.transcribe_audio(model, audio_file_path)
        if transcription is None:
            continue
        success = steps.save_transcription(transcription, transcription_file_path)
        if success is None:
            continue

        lesson_model.update(lesson["lesson_id"], {"transcribed": True})
