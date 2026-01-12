'''Точка входа в приложение. Этот модуль создает экземпляр FastAPI приложения, настраивает шаблоны Jinja2,
регистрирует маршруты и API эндпоинты.'''
from urllib.request import Request

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from api.books import router as books_router

app = FastAPI()
current_dir = Path(__file__).parent
templates = Jinja2Templates(directory=str(current_dir / "templates"))

app.include_router(books_router, tags=["books"], prefix="/books")


@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    '''Главная страница.'''
    context = {
        "request": request,
        "title": "Главная страница",
    }
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/about/", response_class=HTMLResponse, name="about")
async def about(request: Request):
    '''Страница о разработчике.'''
    context = {
        "request": request,
        "title": "О разработчике",
        "student": {"name": "Андрей Переверзев",
                    "age": 25}
    }
    return templates.TemplateResponse(request, "about.html", context)


if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8000, reload=True)
