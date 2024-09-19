import asyncio
import concurrent.futures as cf
import functools
import logging
from typing import Callable, Coroutine, List, Optional, Union

import aiohttp
import whisper
from tqdm import tqdm

import constants
from store.mongo.models.lessons import LessonModel
from transcriptor import steps


def maybe[T, K, U, V](
    fn: Callable[[T], Coroutine[K, U, V]],
) -> Callable[[T], Optional[V]]:
    @functools.wraps(fn)
    async def decorator(*args, **kwargs) -> Optional[V]:
        try:
            return await fn(*args, **kwargs)
        except Exception:
            return None

    return decorator


async def download_video_async(
    session: aiohttp.ClientSession, url: str, lesson_id: str
) -> str:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            file_path = constants.BASE_PATH / f"{lesson_id}.mp4"
            with open(file_path, "wb") as file:
                progress = tqdm(
                    desc=str(file_path),
                    total=total_size,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
                )
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        file.write(chunk)
                        progress.update(len(chunk))
                progress.close()
        return lesson_id
    except Exception as e:
        logging.info("Failed to download video: %s due to %s", lesson_id, e)
        return None


def convert_job(lesson_id: str) -> Optional[str]:
    video_file_path = constants.BASE_PATH / f"{lesson_id}.mp4"
    audio_file_path = constants.BASE_PATH / f"{lesson_id}.mp3"
    try:
        steps.convert_video_to_audio(video_file_path, audio_file_path)
        return lesson_id
    except Exception:
        return None


async def transcript_async(
    config: dict, subject_names: List[str], max_lessons: Union[int | None] = None
):
    constants.BASE_PATH.mkdir(parents=True, exist_ok=True)
    lessons = list(steps.untranscribed_lessons(subject_names, max_lessons))

    # Download videos concurrently
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=min(10, config["MAX_DOWNLOAD_WORKERS"], max_lessons)
        ),
    ) as session:
        download_task = functools.partial(download_video_async, session)
        downloaded_ids = await asyncio.gather(
            *[download_task(lesson["video"], lesson["lesson_id"]) for lesson in lessons]
        )
    logging.info("Downloaded videos: %s", downloaded_ids)

    # Convert video to audio in parallel
    with cf.ProcessPoolExecutor(max_workers=config["MAX_CONVERT_WORKERS"]) as executor:
        converted_ids = executor.map(convert_job, filter(None, downloaded_ids))
    logging.info("Converted videos: %s", list(converted_ids))

    # Transcribe sequentially
    model = whisper.load_model(
        config["MODEL"],
        device=config["DEVICE"],
        download_root=config["CACHE_PATH"],
        in_memory=True,
    )

    results = []
    for lesson_id in converted_ids:
        if lesson_id is None:
            continue
        transcription_file_path = constants.BASE_PATH / f"{lesson_id}.json"
        audio_file_path = constants.BASE_PATH / f"{lesson_id}.mp3"
        transcription = steps.transcribe_audio(model, audio_file_path)
        if transcription is None:
            continue

        steps.save_transcription(transcription, transcription_file_path)
        if transcription is None:
            continue

        results.append(lesson_id)

    logging.info("Transcribed lessons: %s", results)

    # Update lesson statuses
    lesson_model = LessonModel()
    lesson_model.update_many({"_id": {"$in": results}}, {"$set": {"transcribed": True}})


def transcript(
    config: dict, subject_names: List[str], max_lessons: Union[int | None] = None
):
    asyncio.run(transcript_async(config, subject_names, max_lessons))
