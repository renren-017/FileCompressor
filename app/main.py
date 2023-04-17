from fastapi import FastAPI
from app.api.compression import router as compression_router

app = FastAPI()

app.include_router(compression_router, prefix="/compress", tags=["compression"])
