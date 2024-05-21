import json
import logging
from argparse import ArgumentParser
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from mock import MONGO_CLIENT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# capaz mover a un .env despues
PROJECT_ROOT_PATH = Path(__file__).parent.parent
DB_PATH = f"{PROJECT_ROOT_PATH}/vector_db_test"
CORPUS_PATH = f"{PROJECT_ROOT_PATH}/corpus"
CACHE_MODELS_PATH = f"{PROJECT_ROOT_PATH}/models/embeddings"


def load_json(file_path):
    # TODO: depende de como sea el formato de los json y si son muy grandes capaz es mejor hacerlo lazy
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_embedding_model():
    cache_folder = Path(CACHE_MODELS_PATH)
    cache_folder.mkdir(exist_ok=True)

    model_name = "sentence-transformers/all-mpnet-base-v2"
    # otros que podriamos probar
    # > "sentence-transformers/all-MiniLM-L6-v2"
    # > "jinaai/jina-embeddings-v2-base-es"
    return HuggingFaceEmbeddings(
        cache_folder=str(cache_folder),
        model_name=model_name,
        model_kwargs={"device": "cuda:0"},  # 'cpu' si no quieren/pueden GPU
        show_progress=True,
    )


def load_vector_db(folder_path=DB_PATH):
    embedding_model = load_embedding_model()

    if Path(folder_path + "/index.faiss").exists():
        db = FAISS.load_local(
            folder_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )
    else:
        db = seed_vector_db(folder_path, embedding_model)

    return db


def seed_vector_db(
    embedding_model, db_folder_path=DB_PATH, data_folder_path=CORPUS_PATH
):
    all_docs_ids = MONGO_CLIENT["database"]["classes"].find({}, projection={"_id": 1})

    for id in all_docs_ids:
        class_transcript = Path(f"{data_folder_path}/{id}.json")
        if not class_transcript.exists():
            logging.error(f"File {class_transcript} not found!")
            continue

        content = load_json(class_transcript)
        # capaz mover esto adentro del json loader y paralelizar
        texts, metadatas = zip(
            *(
                (
                    item["text"],
                    {"class_id": id, "start": item["start"], "end": item["end"]},
                )
                for item in content
            )
        )

        vectorstore = FAISS.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embedding_model,
        )

    vectorstore.save_local(folder_path=db_folder_path)
    return vectorstore


def drop_vector_db(folder_path=DB_PATH):
    folder_path = Path(folder_path)
    (folder_path / "index.faiss").unlink(missing_ok=True)
    (folder_path / "index.pkl").unlink(missing_ok=True)


def add_document_to_db(db, document):
    raise NotImplementedError


def checkpoint_vector_db(db):
    raise NotImplementedError


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--drop", action="store_true")
    args = parser.parse_args()

    if args.seed:
        logging.info(f"Seeding vector database {DB_PATH} with data from {CORPUS_PATH}")
        seed_vector_db(embedding_model=load_embedding_model())

    if args.drop:
        logging.info(f"Dropping vector database from {DB_PATH}")
        drop_vector_db()
