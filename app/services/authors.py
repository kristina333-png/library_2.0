from fastapi import HTTPException
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate


async def get_all_authors(db: AsyncSessionLocal, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Author).offset(skip).limit(limit))
    return result.scalars().all()


async def get_author_by_id(db: AsyncSessionLocal, author_id: int):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author


async def create_author(db: AsyncSessionLocal, author_data: AuthorCreate):
    new_author = Author(
        full_name=author_data.full_name,
        birth_year=author_data.birth_year,
        country=author_data.country
    )
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author


async def update_author(db: AsyncSessionLocal, author_id: int, author_data: AuthorUpdate):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    if author_data.full_name is not None:
        author.full_name = author_data.full_name
    if author_data.birth_year is not None:
        author.birth_year = author_data.birth_year
    if author_data.country is not None:
        author.country = author_data.country

    await db.commit()
    await db.refresh(author)
    return author


async def delete_author(db: AsyncSessionLocal, author_id: int):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    # Загружаем книги автора
    await db.refresh(author, attribute_names=["books"])
    if author.books and len(author.books) > 0:
        raise HTTPException(status_code=409, detail="Нельзя удалить автора с книгами")

    await db.delete(author)
    await db.commit()
    return {"message": "Автор успешно удален"}