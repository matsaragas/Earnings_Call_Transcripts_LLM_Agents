from fastapi import FastAPI, APIRouter, Request, Depends
import api.endpoints.worker as worker
from core.config import Settings
from langchain_openai import AzureOpenAIEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from langchain.vectorstores import FAISS


ORIGINS = ["http://localhost:8001",
           "http://localhost:5173"]


embeddings = AzureOpenAIEmbeddings(
    azure_deployment="",
    openai_api_version="",
    azure_endpoint="",
    api_key=""
)


settings = Settings()

vector_store = FAISS.load_local(
    settings.VECTOR_DIR,
    embeddings,
    allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever()

app = FastAPI(title=settings.PROJECT_NAME)
api_router = APIRouter(prefix=settings.API_V1_STR)

worker_routes =worker.build(settings, retriever)
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