from fastapi import FastAPI

from app.api.auth import router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(router)