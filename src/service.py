from fastapi import Depends, HTTPException, status

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Question
from src.schemas import QuestionSchema
from src.utils import get_questions_from_service


class QuestionService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
    
    async def is_duplicate(self, id: int) -> bool:
        """Checks if the question already exists in DB.
        Args:
            id (int): question id.
        Raises:
            HTTPException: HTTP_503_SERVICE_UNAVAILABLE.
        Returns:
            bool: is the question duplicate.
        """
        try:
            question = await self.session.scalar(
                select(Question)
                .where(Question.id == id)
            )
            return question is not None
        except Exception as e:
            print(e)  # log error into a console
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Temporary unavailable"
            )
                
    async def add(self, quantity: int) -> QuestionSchema:
        """Saves questions to DB.
        Args:
            quantity (int): question quantity.
        Returns:
            QuestionSchema: last added question.
        """
        questions = await get_questions_from_service(quantity)
        last_added_question = None
        duplicate_counter = 0
        for question in questions:
            if await self.is_duplicate(question.get("id")):
                duplicate_counter += 1
                continue
            new_question = QuestionSchema.model_validate(question)
            await self.session.execute(
                insert(Question)
                .values(**new_question.model_dump())
            )
            await self.session.commit()
            last_added_question = new_question
        if duplicate_counter != 0:
            last_added_question = await self.add(duplicate_counter)
        return last_added_question
