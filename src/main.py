from fastapi import FastAPI

from src.routes.file_upload import router as file_router

app = FastAPI(description="Intelligent Document Processing with RAG and Summarization")

app.include_router(router=file_router)
