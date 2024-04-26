# Quiz API

## Разработано с помощью:
- Python 3.10
- FastAPI - 0.103.2
- PostgreSQL
- SQLAlchemy - 2.0.21
- Pydantic - 2.4.2
- aiohttp - 3.8.6

## Сборка и запуск проекта:
    git clone https://github.com/1ordhokage/api_task.git
Из корневой папки проекта:

    docker-compose up --build

Swagger: `http://0.0.0.0:8000/docs`

P.S. Сборка под Linux и MacOS.

## Реализация:

Получение данных с публичного API :

`src/utils.py`
```Python
async def get_questions_from_service(quantity: int) -> list[dict]:
    """Sends a request to a third-party resource to obtain a list of questions.
    Args:
        quantity (int): number of questions.
    Raises:
        HTTPException: HTTP_503_SERVICE_UNAVAILABLE.
    Returns:
        list[dict]: list of questions.
    """
    try:
        async with aiohttp.ClientSession() as session:
            source = source_settings.URL + str(quantity)
            async with session.get(source, ssl=False) as response:
                return await response.json()
    except aiohttp.ClientConnectorError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Question service is temporary unavailable"
        )
```

Функция для сохранения полученных вопросов. Рекурсивно запрашивает и сохраняет уникальные вопросы, пока количество сохраненных вопросов не будет совпадать с запрашиваемым. Такдже хранит последний сохраненный вопрос (см. требования):

 `src/service.py`
```Python
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
```

## Пример запроса:
```HTTP
POST http://0.0.0.0:8000/questions/?questions_num=100
```

Пример тела ответа - последний добавленный вопрос:

```JSON
{
  "id": 185133,
  "question": "It describes these two angles that tell you how lovely & terrific you are",
  "answer": "complementary",
  "created_at": "2022-12-30T21:25:06.605000Z"
}

```
<img width="1422" alt="swagger_screenshot" src="https://github.com/1ordhokage/api_task/assets/61906886/21819e83-1a77-4b54-8795-e76cad3363f5">




