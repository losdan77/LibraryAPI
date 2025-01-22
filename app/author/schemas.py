from pydantic import BaseModel
from datetime import date


class SAddAuthor(BaseModel):
    name: str
    bio: str | None = None
    date_b: date


class SUpdateAuthorBio(BaseModel):
    id_author: int
    bio: str