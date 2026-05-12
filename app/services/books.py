from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book, Author, Issue
from app.schemas import BookCreate, BookUpdate


async def get_all_books(db: AsyncSession,
                        author_id: int = None,
                        published_year: int = None,
                        title_search: str = None,
                        skip: int = 0,
                        limit: int = 100):
    query = select(Book)

    if author_id is not None:
        query = query.where(Book.author_id == author_id)
    if published_year is not None:
        query = query.where(Book.published_year == published_year)
    if title_search is not None:
        query = query.where(Book.title.ilike(f"%{title_search}%"))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: int):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


async def create_book(db: AsyncSession, book_data: BookCreate):
    author = await db.get(Author, book_data.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    copies_available = book_data.copies_available
    if copies_available is None:
        copies_available = book_data.copies_total

    if copies_available > book_data.copies_total:
        raise HTTPException(status_code=400,
                            detail="Доступных копий не может быть больше общего количества")

    new_book = Book(
        title=book_data.title,
        published_year=book_data.published_year,
        copies_total=book_data.copies_total,
        author_id=book_data.author_id,
        copies_available=copies_available
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book_data.title is not None:
        book.title = book_data.title
    if book_data.published_year is not None:
        book.published_year = book_data.published_year
    if book_data.copies_total is not None:
        if book_data.copies_total < book.copies_available:
            raise HTTPException(status_code=400,
                                detail="Общее количество копий не может быть меньше доступных")
        book.copies_total = book_data.copies_total

    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: int):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    result = await db.execute(
        select(Issue).where(
            Issue.book_id == book_id,
            Issue.returned_at.is_(None)
        )
    )
    active_issue = result.scalar_one_or_none()

    if active_issue:
        raise HTTPException(status_code=409,
                            detail="Нельзя удалить книгу, которая выдана читателю")

    await db.delete(book)
    await db.commit()
    return {"message": "Книга успешно удалена"}


async def decrease_available_copies(db: AsyncSession, book_id: int):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book.copies_available <= 0:
        raise HTTPException(status_code=409, detail="Нет доступных копий")

    book.copies_available -= 1
    await db.commit()
    return book


async def increase_available_copies(db: AsyncSession, book_id: int):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book.copies_available < book.copies_total:
        book.copies_available += 1

    await db.commit()
    return book