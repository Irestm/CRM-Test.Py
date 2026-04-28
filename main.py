import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.routers.client import router as client_router
from api.routers.auth import router as auth_router
from api.routers.task import router as task_router
from core.database import init_db
from src.api.dependencies import get_backup_service
from api.exceptions import http_exception_handler, validation_exception_handler, generic_exception_handler

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

scheduler = AsyncIOScheduler()

async def scheduled_backup():
    backup_service = get_backup_service()
    await backup_service.create_backup()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler.add_job(scheduled_backup, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="CRM API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(client_router)