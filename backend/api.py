import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage

from RAG.rag import rag
from store.mongo.models.lessons import LessonModel

from .models import ChatResponse, Source, UserQuery

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chats = {}


def generate_id():
    return str(len(chats) + 1)


# TODO: async/concurrency


@app.post("/query")
def query(user_query: UserQuery) -> ChatResponse:
    logging.debug(user_query)
    user_question = user_query.query
    conversation_id = user_query.conversation_id

    if conversation_id == "":
        conversation_id = generate_id()

    if conversation_id not in chats:
        chats[conversation_id] = []
    chat_history = chats[conversation_id]

    answer = rag(user_question, chat_history)
    # TODO: HumanMessage handling shouldnt be here in the API
    chat_history.extend([HumanMessage(content=user_question), answer["answer"]])

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
