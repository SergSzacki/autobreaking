from fastapi import FastAPI

from app.core.database import (check_connection)

app = FastAPI(
    title="AutoBreaking API",
    version="0.1.0"
)


@app.get("/")
async def root():
    return {
        "application": "AutoBreaking",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "daabase": await check_connection()
    }
