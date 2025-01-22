from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, intpk, created_at


class Book_issuance(Base):
    __tablename__ = 'book_issuance'

    id: Mapped[intpk]
    issuance_date: Mapped[created_at]
    return_date: Mapped[date] = mapped_column(nullable=False)
    is_return: Mapped[bool] = mapped_column(nullable=False, default=False)
    id_book: Mapped[int] = mapped_column(ForeignKey('book.id'), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    book: Mapped[list['Book']] = relationship(back_populates='book_issuance')
    user: Mapped[list['User']] = relationship(back_populates='book_issuance') 

    __table_args__ = (
        Index('id_book_index', 'id_book'),
        Index('id_user_index', 'id_user'),
        Index('is_return_index', 'is_return'),
    )

    def __str__(self):
        return f'{self.id}'