from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, HttpUrl, NonNegativeFloat


class DefaultConfig(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True
        slots = True


class Source(DefaultConfig):
    lesson_name: str
    subject_name: str
    url: HttpUrl = Field(..., description="URL to the lesson video hosted by OpenFING.")
    timestamps: List[NonNegativeFloat] = Field(
        ...,
        min_length=2,
        description="List of start and end timestamps of the lessons chunks retrieved as context to answer the user query. Timestamps are in seconds from the start of the lesson.",
    )


class ChatResponse(DefaultConfig):
    llm_response: str
    conversation_id: str
    sources: List[Source]


class UserQuery(DefaultConfig):
    query: str = Field(..., description="User question to the LLM.")
    conversation_id: str = Field(..., description="Param to identify conversation.")
    metadata: Optional[Tuple[str, str]] = Field(
        default=None, nullable=True, description="Tuple of (lesson_id, subject_id)"
    )
