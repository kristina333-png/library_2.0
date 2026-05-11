from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services import authors
from app.schemas import AuthorCreate, AuthorUpdate, AuthorResponse

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreate,
    db: AsyncSession = Depends(get_db)
):
    return await authors.create_author(db, author_data)


@router.get("/", response_model=List[AuthorResponse])
async def get_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await authors.get_all_authors(db, skip=skip, limit=limit)


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await authors.get_author_by_id(db, author_id)


@router.patch("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await authors.update_author(db, author_id, author_data)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db)
):
    await authors.delete_author(db, author_id)
    return None