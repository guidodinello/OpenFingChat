from pathlib import Path
from typing import List, Tuple

import pydantic_core
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from store.data.models.lessons import LessonModel

from .models import Query, Response, Source

TEST = True

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat-mu-lemon.vercel.app/"],
    allow_headers=["*"],
)


@app.post("/query")
def query(query: Query) -> Response:
    if TEST:
        with open(Path(__file__).parent / "mock_response.json", "r") as f:
            return Response(**pydantic_core.from_json(f.read()))

    # asumo answer_metadata es una lista de tuplas (lesson_id, lista de timestamps)
    answer_metadata: List[Tuple[str, List[float]]]
    llm_answer, answer_metadata = (
        "stub",
        [("11f", [0.0, 1.0])],
    )  # rag(query.query, query.metadata)

    if not answer_metadata:
        return {"llm_response": llm_answer, "sources": []}

    # Si el retriever devolvio varios chunks de la misma clase los agrupo
    lesson_timestamps = {}
    for lesson_id, timestamps in answer_metadata:
        if lesson_id in lesson_timestamps:
            lesson_timestamps[lesson_id].extend(timestamps)
        else:
            lesson_timestamps[lesson_id] = timestamps

    # capaz preciso convertirlos a ObjectId primero
    lessons_id = list(lesson_timestamps.keys())
    pipeline = [
        {"$match": {"_id": {"$in": lessons_id}}},  # para las lessons
        {  # hacer un join con subjects
            "$lookup": {
                "from": "subjects",
                "localField": "subjectId",
                "foreignField": "_id",
                "as": "subject",
            }
        },
        {"$unwind": "$subject"},
        # quedarse solo con los campos que interesan
        {"$project": {"_id": 1, "name": 1, "url": 1, "subject_name": "$subject.name"}},
    ]

    sources = [
        Source(
            lesson_name=lesson["name"],
            subject_name=lesson["subject_name"],
            url=lesson["url"],
            timestamps=lesson_timestamps[lesson["_id"]],
        )
        for lesson in LessonModel().collection.aggregate(pipeline)
    ]

    return {"llm_response": llm_answer, "sources": sources}
