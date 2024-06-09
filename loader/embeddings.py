import logging
from os import PathLike
from pathlib import Path
from typing import Self  # precisa python>=3.11

from langchain_community.embeddings import HuggingFaceEmbeddings
from torch import cuda


class Embeddings:
    _instance = None

    @classmethod
    def load(cls, cache_path: PathLike) -> Self:
        if cls._instance is None:
            cls._instance = cls._load_embedding_model(cache_path=cache_path)
        return cls._instance

    @staticmethod
    def _load_embedding_model(cache_path):
        cache_folder = Path(cache_path) / "embeddings"
        if not cache_folder.exists():
            logging.info(f"Creating cache folder at {cache_folder}")
            cache_folder.mkdir(exist_ok=True, parents=True)

        device = "cuda:0" if cuda.is_available() else "cpu"

        model_name = "sentence-transformers/all-mpnet-base-v2"
        # otros que podriamos probar
        # > "sentence-transformers/all-MiniLM-L6-v2"
        # > "jinaai/jina-embeddings-v2-base-es"
        return HuggingFaceEmbeddings(
            cache_folder=str(cache_folder),
            model_name=model_name,
            model_kwargs={"device": device},
            show_progress=True,
        )
