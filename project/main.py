import logging

import uvicorn
from fastapi import Depends, FastAPI

from logger_settings import stream_handler, file_handler
from src.core.config import settings
from src.api import router as main_router
from src.auth.auth_router import router as auth_router

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(main_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    logger.debug("Root is responding")
    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
