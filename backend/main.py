from fastapi import FastAPI, APIRouter, Request, Depends
from api.endpoints import worker
from core.config import Settings
from fastapi.middleware.cors import CORSMiddleware

ORIGINS = ["http://localhost:8001",
           "http://localhost:5173"]

settings = Settings()
app = FastAPI(title=settings.PROJECT_NAME)
api_router = APIRouter(settings.API_V1_STR)

worker_routes =worker.build(settings)
api_router.include_router(worker_routes, tags=["Plugin Worker"])
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")