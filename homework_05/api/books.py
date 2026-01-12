'''API для работы с книгами. Этот модуль предоставляет REST API эндпоинты для управления коллекцией книг.
Включает операции создания, чтения и поиска книг.'''

from pydantic import BaseModel
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.templating import Jinja2Templates


class Book(BaseModel):
    title: str
    author: str
    tag: str
    year: int


book_list = [
    Book(
        title="Чистый код",
        author="Роберт Мартин",
        tag="Создание, анализ, рефакторинг кода",
        year=2008,
    ),
    Book(
        title="Грокаем алгоритмы",
        author="Адитья Бхаргава",
        tag="Главные алгоритмы, позволяющие ускорить работу программ и упростить код",
        year=2016,
    ),
    Book(
        title="Чистый python",
        author="Дэн Бейдер",
        tag="Тонкости программирования на python",
        year=2018,
    )
]

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_model=list[Book], name="book_list")
async def book_list(
        title: str = Query(None, description="Название книги.")
):
    '''Получить список книг.'''
    result = book_list
    if title is not None:
        result = [book for book in result if title in book.title]
    return result


@router.get("/{book_id}/", response_model=Book, name="book_detail")
async def book_detail(book_id: int):
    '''Получить детальную информацию о книге.'''
    book_id -= 1
    if book_id < 0 or book_id > len(book_list):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга с таким id не найдена.")
    return book_list[book_id]


@router.post("/", response_model=Book, name="book_create")
async def book_create(book: Book):
    '''Добавить книгу.'''
    for b in book_list:
        if b.title == book.title:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такая книга уже есть.")
    book_list.append(book)
    return book
