from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services import books
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
):
    return await books.create_book(db, book_data)


@router.get("/", response_model=List[BookResponse])
async def get_books(
    author_id: Optional[int] = Query(None, description="Фильтр по ID автора"),
    published_year: Optional[int] = Query(None, description="Фильтр по году публикации"),
    title_search: Optional[str] = Query(None, description="Поиск по названию (частичное совпадение)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await books.get_all_books(
        db,
        author_id=author_id,
        published_year=published_year,
        title_search=title_search,
        skip=skip,
        limit=limit
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await books.get_book_by_id(db, book_id)


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await books.update_book(db, book_id, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    await books.delete_book(db, book_id)
    return None