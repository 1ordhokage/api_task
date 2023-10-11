from fastapi import FastAPI

from src.api import router as question_router


app = FastAPI(
    title="Quiz App",
    description="Bewise.ai test task",
    version="0.0.1",
)

app.include_router(question_router)
