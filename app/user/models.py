from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, intpk, str_not_null, created_at
from app.book_issuance.models import Book_issuance


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str_not_null]
    name: Mapped[str_not_null]
    role: Mapped[str] = mapped_column(nullable=False, default='reader')
    book_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[created_at]

    book_issuance: Mapped[list['Book_issuance']] = relationship(back_populates='user') 

    def __str__(self):
        return f'{self.email}'