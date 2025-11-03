from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from app.config import get_settings
from app.routers import tasks

config = get_settings()
templates = Jinja2Templates(directory=config.templates_dir)

app = FastAPI()
app.mount(
    '/static',
    StaticFiles(directory=config.static_dir),
    name='static',
)
app.include_router(tasks.router)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def read_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        # context={},
    )


@app.get('/favicon.ico', include_in_schema=False)
async def favicon_ico():
    favicon_path = config.static_dir / 'favicon.ico'
    return FileResponse(favicon_path)


@app.get('/favicon.png', include_in_schema=False)
async def favicon_png():
    favicon_path = config.static_dir / 'favicon.png'
    return FileResponse(favicon_path)


@app.get('/health', tags=['health'])
async def health_check():
    return {'status': 'ok'}
