import json
import logging
import os
from typing import Iterable, Iterator, List, Optional, Union

import pymongo.command_cursor
import whisper
from moviepy.editor import VideoFileClip

from store.mongo.models.subjects import SubjectModel


def convert_video_to_audio(
    video_file_path: os.PathLike, audio_file_path: os.PathLike
) -> Optional[bool]:
    try:
        video = VideoFileClip(str(video_file_path))
        audio = video.audio
        audio.write_audiofile(str(audio_file_path))
        audio.close()
        video.close()
        logging.info("Audio extracted and saved to:  %s", audio_file_path)
        return True
    except Exception as e:
        logging.error("Error converting video to audio:  %s", e)
        return None


def transcribe_audio(
    model: whisper.Whisper,
    audio_file_path: os.PathLike,
) -> Optional[Iterator[dict]]:
    try:
        result = model.transcribe(str(audio_file_path), language="es", fp16=True)
        segments = (
            {
                "text": segment["text"],
                "start": segment["start"],
                "end": segment["end"],
            }
            for segment in result["segments"]
        )

        logging.info("Lesson %s transcribed", audio_file_path)
        return segments
    except Exception as e:
        logging.error("Error transcribing audio:  %s", e)
        return None


def untranscribed_lessons(
    subject_names: List[str], max_lessons: Union[int, None] = None
) -> pymongo.command_cursor.CommandCursor:
    # pipeline to get all unstranscribed lessons for the given subjects
    pipeline = [
        {"$match": {"name": {"$in": subject_names}}},
        {
            "$lookup": {
                "from": "lessons",
                "localField": "_id",
                "foreignField": "subjectId",
                "as": "lessons",
            }
        },
        {"$unwind": "$lessons"},
        {"$match": {"lessons.transcribed": False}},
        {
            "$project": {
                "_id": 0,
                "lesson_id": "$lessons._id",
                "video": "$lessons.video",
            }
        },
    ]
    if max_lessons:
        pipeline.append({"$limit": max_lessons})
    return SubjectModel().collection.aggregate(pipeline)


def save_transcription(
    transcription: Iterable[dict], transcription_file_path: os.PathLike
) -> Optional[bool]:
    try:
        with open(transcription_file_path, "w", encoding="utf-8") as f:
            json.dump(list(transcription), f, ensure_ascii=False)
        logging.info("Transcription saved to:  %s", transcription_file_path)
        return True
    except Exception as e:
        logging.error("Error saving transcription:  %s", e)
        return None
