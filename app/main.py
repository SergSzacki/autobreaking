from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import cars, parts
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

app = FastAPI(title=f"{settings.APP_NAME} - Cars API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(cars.router, prefix="/api")
app.include_router(parts.router, prefix="/api")
