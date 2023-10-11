from datetime import datetime

from pydantic import BaseModel


class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
