import uvicorn
from fastapi import Depends, FastAPI

from core.config import settings
from api import router as main_router
from auth.auth_router import router as auth_router


app = FastAPI()

app.include_router(main_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
