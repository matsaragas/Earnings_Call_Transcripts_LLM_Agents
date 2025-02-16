from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS

from config import Settings
from core.controller import Controller


settings = Settings()
controller = Controller(settings=settings)