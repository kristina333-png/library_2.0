from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

current_year = date.today().year


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    published_year: int = Field(..., gt=1000, le=current_year+1)
    copies_total: int = Field(..., ge=1)
    author_id: int = Field(..., ge=1)


class BookCreate(BookBase):
    copies_available: Optional[int] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    published_year: Optional[int] = None
    copies_total: Optional[int] = None


class BookResponse(BookBase):
    id: int
    copies_available: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True