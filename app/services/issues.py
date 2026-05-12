from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.models import Book, Issue
from app.schemas import IssueCreate


async def get_issue_by_id(db: AsyncSession, issue_id: int):
    issue = await db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Выдача не найдена")
    return issue


async def get_all_issues(db: AsyncSession, status: str = None, borrower_name: str = None, skip: int = 0,
                         limit: int = 100):
    query = select(Issue)

    if status == "active":
        query = query.where(Issue.returned_at.is_(None))
    elif status == "closed":
        query = query.where(Issue.returned_at.is_not(None))

    if borrower_name:
        query = query.where(Issue.borrower_name.ilike(f"%{borrower_name}%"))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_issue(db: AsyncSession, issue_data: IssueCreate):
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

    due_at = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    due_at = due_at.replace(day=due_at.day + issue_data.days_to_return)

    if due_at < datetime.now():
        raise HTTPException(status_code=400, detail="Дата возврата не может быть в прошлом")

    book.copies_available -= 1

    new_issue = Issue(
        book_id=issue_data.book_id,
        borrower_name=issue_data.borrower_name,
        due_at=due_at,
        returned_at=None
    )

    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    return new_issue


async def return_book(db: AsyncSession, issue_id: int):
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