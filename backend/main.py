from fastapi import FastAPI, APIRouter, Request, Depends
from core.config import Settings

settings = Settings()


app = FastAPI(title=settings.PROJECT_NAME)

api_router = APIRouter(settings.API_V1_STR)
