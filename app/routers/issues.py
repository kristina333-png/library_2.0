from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services import issues
from app.schemas import IssueCreate, IssueResponse

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
        issue_data: IssueCreate,
        db: AsyncSession = Depends(get_db)
):
    return await issues.create_issue(db, issue_data)


@router.get("/", response_model=List[IssueResponse])
async def get_issues(
        status: Optional[str] = Query(None,
                                      description="active - активные, closed - закрытые, или не указывать"),
        borrower_name: Optional[str] =
        Query(None, description="Поиск по имени читателя (частичное совпадение)"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):

    if status is not None and status not in ["active", "closed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Статус должен быть 'active' или 'closed'"
        )

    return await issues.get_all_issues(
        db,
        status=status,
        borrower_name=borrower_name,
        skip=skip,
        limit=limit
    )


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
        issue_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await issues.get_issue_by_id(db, issue_id)


@router.post("/{issue_id}/return", response_model=IssueResponse)
async def return_book(
        issue_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await issues.return_book(db, issue_id)