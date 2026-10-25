from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.routers.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="User Registration API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users_router)

@app.get("/")
def read_root():
    return {"message": "Hello"}