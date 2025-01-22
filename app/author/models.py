from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, intpk, str_not_null, str_null


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[intpk]
    name: Mapped[str_not_null]
    bio: Mapped[str_null]
    date_b: Mapped[date] = mapped_column(nullable=False)

    book: Mapped[list['Book']] = relationship(back_populates='author',
                                              secondary='book_author')

    def __str__(self):
        return f'{self.name}'