from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrower_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    loaned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    returned_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    book: Mapped["Book"] = relationship("Book", back_populates="issues")