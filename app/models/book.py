from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False)
    copies_total: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    copies_available: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    issues: Mapped[List["Issue"]] = relationship(
        "Issue",
        back_populates="book",
        cascade="all, delete-orphan"
    )