import functools
import json
import logging
import os
from concurrent import futures
from os import PathLike
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

from store.data.models.lessons import LessonModel

from .embeddings import Embeddings

load_dotenv(override=True)

PROJECT_ROOT_PATH = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT_PATH / os.environ.get("VDB_PATH")
DATA_PATH = PROJECT_ROOT_PATH / os.environ.get("DATA_PATH")
CACHE_PATH = PROJECT_ROOT_PATH / os.environ.get("CACHE_PATH")


class VectorStore:
    def __init__(
        self,
        embedding_model: Optional[Embeddings] = None,
        persistence_path: PathLike = DB_PATH,
        data_path: PathLike = DATA_PATH,
        seed_on_init: bool = True,
    ):
        self.embedding_model = embedding_model or Embeddings.load(cache_path=CACHE_PATH)
        self.path = Path(persistence_path)
        self.data_path = Path(data_path)
        self.db = None
        if seed_on_init:
            self._load_vectorstore()

    def _load_vectorstore(self):
        if (self.path / "index.faiss").exists():
            logging.info(f"Loading existing vectorstore from {self.path}")
            self.db = FAISS.load_local(
                self.path,
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True,
            )
        else:
            logging.info(f"Creating new vectorstore at {self.path}")
            self.seed(self.data_path)

    def seed(self, data_path: PathLike) -> None:
        """
        Seed the vectorstore with the whisper-segmented-json files inside data_path folder
        """
        data_path = data_path or self.data_path

        if not Path(data_path).exists():
            logging.error(f"Data folder {data_path} does not exist!")
            return self
        logging.info(f"Seeding vectorstore with data from {data_path}")

        lessons_id = LessonModel().getAll(
            filters={"transcribed": True},
            projection={"_id": 1},
        )
        if not lessons_id:
            logging.error("No transcribed lessons returned from the database!")
            # si no hay lessons marcadas como transcriptas, para testear se puede usar el mock
            # from mock import MONGO_CLIENT
            # lessons_id = MONGO_CLIENT["database"]["classes"].find(
            #     {"transcribed": True},
            #     projection={"_id": 1},
            # )
            return self

        job = functools.partial(process_transcript, data_path)
        with futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(job, id) for id in lessons_id]

            for res in futures.as_completed(results):
                result = res.result()
                if result is not None:
                    text, metadata = result

                    vectorstore = FAISS.from_texts(
                        texts=text,
                        metadatas=metadata,
                        embedding=self.embedding_model,
                    )

        if not self.db:
            self.db = vectorstore
        else:
            self.db.merge_from(vectorstore)

        vectorstore.save_local(folder_path=self.path)

    def drop(self) -> None:
        logging.info(f"Dropping vector database from {self.path}")
        (self.path / "index.faiss").unlink(missing_ok=True)
        (self.path / "index.pkl").unlink(missing_ok=True)


def process_transcript(data_folder: PathLike, lesson_id: str) -> Optional[tuple]:
    class_transcript = Path(f"{data_folder}/{lesson_id}.json")
    if not class_transcript.exists():
        logging.error(
            f"Lesson is marked as transcribed but file {class_transcript} not found!"
        )
        return None

    # TODO: asumi que los archivos segmentados estan guardados localmente
    with open(class_transcript, "r", encoding="utf-8") as f:
        content = json.load(f)

    texts, metadatas = zip(
        *(
            (
                item["text"],
                {"lesson_id": lesson_id, "start": item["start"], "end": item["end"]},
            )
            for item in content["segments"]
        )
    )
    return texts, metadatas
