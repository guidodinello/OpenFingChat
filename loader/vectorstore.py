import functools
import json
import logging
from concurrent import futures
from os import PathLike
from pathlib import Path
from typing import Optional

import pymongo
from langchain_community.vectorstores import FAISS

import constants
from store.mongo.models.lessons import LessonModel

from .embeddings import Embeddings


class VectorStore:
    def __init__(
        self,
        embedding_model: Optional[Embeddings] = None,
        persistence_path: PathLike = constants.VDB_PATH,
        data_path: PathLike = constants.DATA_PATH,
        seed_on_init: bool = True,
    ):
        self.embedding_model = embedding_model or Embeddings.load(
            cache_path=constants.CACHE_PATH
        )
        self.path = Path(persistence_path)
        self.data_path = Path(data_path)
        self.db = None
        if seed_on_init:
            self._load_vectorstore()

    def _load_vectorstore(self):
        if (self.path / "index.faiss").exists():
            logging.info("Loading existing vectorstore from  %s", self.path)
            self.db = FAISS.load_local(
                self.path,
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True,
            )
        else:
            logging.info("Creating new vectorstore at  %s", self.path)
            self.seed(self.data_path)

    def seed(self, data_path: PathLike) -> None:
        """
        Seed the vectorstore with the whisper-segmented-json files inside data_path folder
        """
        data_path = data_path or self.data_path

        if not Path(data_path).exists():
            logging.error("Data folder  %s  does not exist!", data_path)
            return self
        logging.info("Seeding vectorstore with data from  %s", data_path)

        lessons_meta = transcribed_lessons()

        if not lessons_meta:
            logging.error("No transcribed lessons returned from the database!")
            # si no hay lessons marcadas como transcriptas, para testear se puede usar el mock
            # from .mock import MONGO_CLIENT

            # lessons_id = MONGO_CLIENT["database"]["classes"].find(
            #     {"transcribed": True},
            #     projection={"_id": 1},
            # )
            return self

        texts = []
        metadatas = []

        job = functools.partial(process_transcript, data_path)
        with futures.ThreadPoolExecutor(max_workers=6) as executor:
            results = [executor.submit(job, meta) for meta in lessons_meta]

            for res in futures.as_completed(results):
                result = res.result()
                if result is not None:
                    text, metadata = result
                    texts.extend(text)
                    metadatas.extend(metadata)

        vectorstore = FAISS.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=self.embedding_model,
        )

        if not self.db:
            self.db = vectorstore
        else:
            self.db.merge_from(vectorstore)

        vectorstore.save_local(folder_path=self.path)

    def drop(self) -> None:
        logging.info("Dropping vector database from  %s", self.path)
        (self.path / "index.faiss").unlink(missing_ok=True)
        (self.path / "index.pkl").unlink(missing_ok=True)


def concatenate_segments(segments, max_length):
    concatenated_segments = []
    current_segment = None

    for segment in segments:
        if current_segment is None:
            current_segment = segment
        else:
            new_length = (
                current_segment["end"]
                - current_segment["start"]
                + segment["end"]
                - segment["start"]
            )
            if new_length <= max_length:
                current_segment["text"] += " " + segment["text"]
                current_segment["end"] = segment["end"]
            else:
                concatenated_segments.append(current_segment)
                current_segment = segment

    if current_segment is not None:
        concatenated_segments.append(current_segment)

    return concatenated_segments


def process_transcript(data_folder: PathLike, lesson_meta: dict) -> Optional[tuple]:
    class_transcript = Path(f"{data_folder}/{lesson_meta["_id"]}.json")

    if not class_transcript.exists():
        logging.error(
            "Lesson is marked as transcribed but file %s not found!", class_transcript
        )
        return None

    with open(class_transcript, encoding="utf-8") as f:
        content = json.load(f)

    if not isinstance(content, list):
        logging.error(
            "Invalid structure in file %s. Expected a list of segments.",
            class_transcript,
        )
        return None

    # Concatenate segments before processing
    max_length = 120  # Set an appropriate max length for concatenation
    concatenated_segments = concatenate_segments(content, max_length)

    texts, metadatas = zip(
        *(
            (
                item["text"],
                {
                    "lesson_id": str(lesson_meta["_id"]),
                    "start": str(item["start"]),
                    "end": str(item["end"]),
                    "subject": lesson_meta["subject_name"],
                    "lesson": lesson_meta["name"],
                },
            )
            for item in concatenated_segments
        )
    )
    return texts, metadatas


def transcribed_lessons() -> pymongo.command_cursor.CommandCursor:
    pipeline = [
        {
            "$match": {
                "transcribed": True,
            }
        },
        {
            "$lookup": {
                "from": "subjects",
                "localField": "subjectId",
                "foreignField": "_id",
                "as": "subject",
            }
        },
        {"$unwind": "$subject"},
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "subject_name": "$subject.name",
            }
        },
    ]
    return LessonModel().collection.aggregate(pipeline)
