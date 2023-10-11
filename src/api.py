from fastapi import APIRouter, Depends, Query, status

from src.schemas import QuestionSchema
from src.service import QuestionService


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "/",
    response_model=QuestionSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_question(
    questions_num: int = Query(le=100),
    service: QuestionService = Depends()
) -> QuestionSchema:
    """Path operation function for adding questions to DB.
    Args:
        quantity (int): question quantity. Defaults to Query(le=100).
        service (QuestionService): business logic for questions.
    Returns:
        QuestionSchema: last added question.
    """
    return await service.add(questions_num)
