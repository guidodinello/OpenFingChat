import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

OPENFING_URL = os.getenv("OPENFING_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

CACHE_PATH = pathlib.Path(os.getenv("CACHE_PATH"))
VDB_PATH = pathlib.Path(os.getenv("VDB_PATH"))
DATA_PATH = pathlib.Path(os.getenv("DATA_PATH"))

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MONGO_ROOT_USER = os.getenv("MONGO_ROOT_USER")
MONGO_ROOT_PASSWORD = os.getenv("MONGO_ROOT_PASSWORD")
MONGOEXPRESS_LOGIN = os.getenv("MONGOEXPRESS_LOGIN")
MONGOEXPRESS_PASSWORD = os.getenv("MONGOEXPRESS_PASSWORD")

MONGODB_URI = f"mongodb://{MONGO_ROOT_USER}:{MONGO_ROOT_PASSWORD}@localhost:27017"
BASE_PATH = pathlib.Path(os.getenv("BASE_PATH"))
CONFIG_FILE = pathlib.Path(__file__)
