from typing import List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, NonNegativeFloat


class DefaultConfig(BaseModel):
    class Config:
        extra = "forbid"  # no extra fields allowed
        frozen = True  # make the objects immutable
        slots = True


class Source(DefaultConfig):
    lesson_name: str
    subject_name: str
    url: HttpUrl = Field(..., description="URL to the lesson video hosted by OpenFING.")
    # es una lista por si son chunks consecutivos de la misma clase
    # tambien alcanzaria con una tupla (start_chunk1, end_chunkN)
    timestamps: List[NonNegativeFloat] = Field(
        ...,
        min_length=2,
        description="List of start and end timestamps of the lessons chunks retrieved as context to answer the user query. Timestamps are in seconds from the start of the lesson.",
    )


class ChatResponse(DefaultConfig):
    llm_response: str
    sources: List[Source]  # [info_lesson_1, info_lesson_2, ...]


class UserQuery(DefaultConfig):
    query: str = Field(..., description="User question to the LLM.")
    metadata: Optional[Tuple[str, str]] = Field(
        default=None, nullable=True, description="Tuple of (lesson_id, subject_id)"
    )  # con solo lesson_id tmbn alcanzaria

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "query": "This is a user question to the LLM",
                    "metadata": ["11f2", "12g3"],
                },
                {
                    "query": "This is a user question to the LLM",
                    "metadata": None,
                },
                {
                    "query": "This is a user question to the LLM",
                },
            ]
        }
    )
