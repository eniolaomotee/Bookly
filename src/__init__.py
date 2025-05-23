from fastapi import FastAPI, status
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from src.headers import header_router
from contextlib import asynccontextmanager
from src.db.db import init_db
from src.errors import register_all_errors
from src.middleware import register_middleware


# determines which code runs before and after the server starts and stops.
@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting")
    from src.db.models import Book
    await init_db()
    yield 
    print(f"server has been stopped")


version = "v1"

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web Service",
    version=version,
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
    openapi_url=f"{version_prefix}/openapi.json",
)



register_all_errors(app)

register_middleware(app)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router,prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tags_router,prefix=f"/api/{version}/tags", tags=["Tags"])
app.include_router(header_router,prefix=f"/api/{version}/headers", tags=["Get Headers"])