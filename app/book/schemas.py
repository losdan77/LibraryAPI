from pydantic import BaseModel
from datetime import date


class SAddBook(BaseModel):
    name: str
    description: str | None = None
    date_pub: date | None = None
    count_avaliable_copies: int
    genre: str | None = None
    id_author: list[int]


class SAddAuthor(BaseModel):
    name: str
    bio: str | None = None
    date_b: date


class SUpdateCountAvaliableCopies(BaseModel):
    id_book: int
    count_avaliable_copies: int