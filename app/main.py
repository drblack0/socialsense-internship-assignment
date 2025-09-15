from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.scheduler.post_scheduler import schedule_checker
import asyncio

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(schedule_checker())


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"message": "Welcome to the LinkedIn Analytics Backend"}
