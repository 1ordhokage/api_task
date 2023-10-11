import aiohttp

from fastapi import HTTPException, status

from src.config import source_settings


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
