from pydantic import BaseModel
from datetime import date


class SIssuanceBook(BaseModel):
    id_book: int
    return_date: date
