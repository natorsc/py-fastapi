from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config.Settings import get_settings
from app.database.db import create_db_and_tables
from app.routers.user import router as user_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title='API title',
    description='API description',
    version=settings.version,
    lifespan=lifespan,
)
app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')

app.include_router(user_router)


@app.get('/')
async def root():
    return {'msg': 'Hello World!'}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(path='favicon.ico')
