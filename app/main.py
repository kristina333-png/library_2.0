from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.routers.authors import router as authors_router
from app.routers.books import router as books_router
from app.routers.issues import router as issues_router

from app.database import engine, Base

app = FastAPI(
    title="Library Service",
    description="API для управления библиотекой",
    version="1.0.0"
)

@app.on_event("startup")
async def init_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(authors_router)
app.include_router(books_router)
app.include_router(issues_router)

@app.get("/")
async def root():
    return {"message": "Library Service API", "docs": "/docs"}