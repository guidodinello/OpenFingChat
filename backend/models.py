from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, HttpUrl, NonNegativeFloat


class Source(BaseModel):
    lesson_name: str
    subject_name: str
    url: HttpUrl  # link al video en openfing
    # es una lista por si son chunks consecutivos de la misma clase
    # tambien alcanzaria con una tupla (start_chunk1, end_chunkN)
    timestamps: List[NonNegativeFloat] = Field(min_length=2)


class Response(BaseModel):
    llm_response: str
    sources: List[Source]  # [info_lesson_1, info_lesson_2, ...]


class Query(BaseModel):
    query: str  # pregunta del user
    metadata: Optional[Tuple[str, str]] = Field(
        default=None, nullable=True, description="Tuple of (lesson_id, subject_id)"
    )  # con solo lesson_id tmbn alcanzaria

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "This is a user question to the LLM",
                    "metadata": ("11f2", "12g3"),
                }
            ]
        }
    }
