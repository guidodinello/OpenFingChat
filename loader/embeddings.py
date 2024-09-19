import logging
from os import PathLike
from pathlib import Path

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from torch import cuda


class Embeddings:
    _instance = None

    @classmethod
    def load(cls, cache_path: PathLike):
        if cls._instance is None:
            cls._instance = cls._load_embedding_model(cache_path=cache_path)
        return cls._instance

    @staticmethod
    def _load_embedding_model(cache_path):
        cache_folder = Path(cache_path) / "embeddings"
        if not cache_folder.exists():
            logging.info("Creating cache folder at  %s", cache_folder)
            cache_folder.mkdir(exist_ok=True, parents=True)

        device = "cuda:0" if cuda.is_available() else "cpu"

        # https://huggingface.co/BAAI/bge-large-en/discussions/15
        model_name = "BAAI/bge-m3"
        return HuggingFaceBgeEmbeddings(
            cache_folder=str(cache_folder),
            model_name=model_name,
            model_kwargs={"device": device},
        )
