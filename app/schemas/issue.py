from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IssueBase(BaseModel):
    book_id: int = Field(..., gt=0)
    borrower_name: str = Field(..., min_length=1)


class IssueCreate(IssueBase):
    days_to_return: int = Field(14, gt=0, le=365)


class IssueResponse(IssueBase):
    id: int
    loaned_at: datetime
    due_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IssueReturnResponse(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    loaned_at: datetime
    due_at: datetime
    returned_at: datetime
    message: str = "Книга успешно возвращена"

    class Config:
        from_attributes = True