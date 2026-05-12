from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.authors import router as authors_router
from app.routers.books import router as books_router
from app.routers.issues import router as issues_router
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Library Service",
    description="API для управления библиотекой",    version="1.0.0",
    lifespan=lifespan
)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(issues_router)

@app.get("/")
async def root():
    return {"message": "Library Service API", "docs": "/docs"}