from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

current_year = date.today().year


class AuthorBase(BaseModel):
    full_name: str = Field(..., min_length=1)
    birth_year: Optional[int] = Field(None, gt=1800, le=current_year)
    country: Optional[str] = Field(None, min_length=1)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_year: Optional[int] = None
    country: Optional[str] = None


class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True