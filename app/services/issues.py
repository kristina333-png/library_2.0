from datetime import datetime
from sqlalchemy import select

from fastapi import HTTPException

from app.database import AsyncSessionLocal
from app.models import Book, Issue
from app.schemas import IssueCreate

async def get_issue_by_id(db: AsyncSessionLocal, issue_id: int):
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Выдача не найдена")
    return issue


async def create_issue(db: AsyncSessionLocal, issue_data: IssueCreate):

    result = await db.execute(
        select(Book)
        .where(Book.id == issue_data.book_id)
        .with_for_update()
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book.copies_available <= 0:
        raise HTTPException(status_code=409, detail="Нет доступных копий книги")

    if issue_data.due_at < datetime.now():
        raise HTTPException(status_code=400, detail="Дата возврата не может быть в прошлом")

    book.copies_available -= 1

    new_issue = Issue(
        book_id=issue_data.book_id,
        reader_name=issue_data.borrower_name,
        due_at=issue_data.due_at,
        returned_at=None
    )

    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    return new_issue


async def return_book(db: AsyncSessionLocal, issue_id: int):
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Выдача не найдена")

    if issue.returned_at is not None:
        raise HTTPException(status_code=409, detail="Книга уже возвращена")

    result = await db.execute(
        select(Book)
        .where(Book.id == issue.book_id)
        .with_for_update()
    )
    book = result.scalar_one()

    if book.copies_available < book.copies_total:
        book.copies_available += 1

    issue.returned_at = datetime.now()

    await db.commit()
    await db.refresh(issue)
    return issue