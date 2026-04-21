from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models.base import Base
from app.routers import users, calculations


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Module 12 Assignment — KV",
    description="User registration/login + Calculation BREAD endpoints",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
def index():
    return {"message": "Module 12 API is running!"}


app.include_router(users.router)
app.include_router(calculations.router)
