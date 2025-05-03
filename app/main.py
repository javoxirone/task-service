from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.db.base import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    init_db()
    print("Database tables created if they didn't exist")
    yield
    # Clean up resources at shutdown if needed
    print("Shutting down application")

# Create FastAPI app with lifespan handler
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
app.include_router(auth_router)
app.include_router(tasks_router)