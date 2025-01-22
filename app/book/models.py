from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, intpk, str_not_null, str_null
from app.author.models import Author


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[intpk]
    name: Mapped[str_not_null]
    description: Mapped[str_null]
    date_pub: Mapped[date] = mapped_column(nullable=True)
    count_avaliable_copies: Mapped[int] = mapped_column(nullable=False, default=0)
    genre: Mapped[str_null]

    author: Mapped[list['Author']] = relationship(back_populates='book',
                                                  secondary='book_author')
    book_issuance: Mapped[list['Book_issuance']] = relationship(back_populates='book') 

    def __str__(self):
        return f'{self.name}'
    

class Book_author(Base):
    __tablename__ = 'book_author'

    id_book: Mapped[int] = mapped_column(
        ForeignKey('book.id', ondelete='CASCADE'),
        primary_key=True,
    )
    id_author: Mapped[int] = mapped_column(
        ForeignKey('author.id', ondelete='CASCADE'),
        primary_key=True,
    )
