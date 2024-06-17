import logging


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage

from RAG.rag import rag
from store.data.models.lessons import LessonModel

from .models import ChatResponse, Source, UserQuery

TEST = False

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat-mu-lemon.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chats = {}


def generate_id():
    return str(len(chats) + 1)


@app.post("/query")
def query(query: UserQuery) -> ChatResponse:
    logging.debug(query)
    input = query.query
    conversation_id = query.conversation_id

    # TODO: segun lo poco que mire el front, el conversation_id es un string vacio la primera vez
    if conversation_id == "":
        conversation_id = generate_id()

    if conversation_id not in chats:
        chats[conversation_id] = []
    chat_history = chats[conversation_id]

    answer = rag(input, chat_history)
    chat_history.extend([HumanMessage(content=input), answer["answer"]])

    lessons = LessonModel()
    sources = []
    for doc in answer["context"]:
        metadata = doc.metadata
        lesson = lessons.get(metadata["lesson_id"], True)
        sources.append(
            Source(
                lesson_name=lesson["name"],
                subject_name=lesson["subject"]["name"],
                url=lesson["url"],
                timestamps=[metadata["start"], metadata["end"]],
            )
        )

    return {
        "llm_response": answer["answer"],
        "sources": sources,
        "conversation_id": conversation_id,
    }
