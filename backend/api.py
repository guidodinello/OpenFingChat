from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from RAG.rag import rag
from store.data.models.lessons import LessonModel

from .models import ChatResponse, Source, UserQuery

TEST = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat-mu-lemon.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query")
def query(query: UserQuery) -> ChatResponse:
    print(query)
    input = query.query # user query input
    conversation_id = query.conversation_id # to keep track of conversation (return it)

    # hay que manejar la memoria con el conversation_id
    chat_history = []
    answer = rag(input, chat_history)
    # print("context", answer["context"])
    
    # CAMBIA TODO LO QUE QUIERAS DE ESTA PARTE

    lessons = LessonModel()
    sources = []
    for doc in answer["context"]:
        metadata = doc.metadata
        lesson = lessons.get(metadata["lesson_id"],True)
        sources.append(Source(
            lesson_name=lesson["name"],
            subject_name=lesson["subject"]["name"],
            url=lesson["url"],
            timestamps=[metadata["start"], metadata["end"]]
        ))

    return {
        "llm_response": answer["answer"], 
        "sources": sources,
        "conversation_id": conversation_id
    }
