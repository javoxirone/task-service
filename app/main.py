from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(auth_router)
app.include_router(tasks_router)