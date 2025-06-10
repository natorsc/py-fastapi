from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from app.config import get_settings
from app.database import create_db_and_tables
from app.routers import tasks

config = get_settings()
templates = Jinja2Templates(directory=config.base_dir / 'templates')

app = FastAPI()
app.mount(
    '/static',
    StaticFiles(directory=config.base_dir / 'static'),
    name='static',
)
app.include_router(tasks.router)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def read_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        # context={},
    )


@app.get('/favicon', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.png')


@app.get('/health', tags=['health'])
async def health_check():
    return {'status': 'ok'}
