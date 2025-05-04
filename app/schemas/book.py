from typing import Optional, List
from pydantic import BaseModel

from app.schemas.author import AuthorResponse
from app.schemas.category import CategoryResponse


class BookBase(BaseModel):
    title: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    total_copies: int = 1
    category_id: Optional[int] = None


class BookCreate(BookBase):
    author_ids: List[int]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    category_id: Optional[int] = None
    author_ids: Optional[List[int]] = None


class BookResponse(BookBase):
    book_id: int
    available_copies: int
    category: Optional[CategoryResponse] = None
    authors: List[AuthorResponse] = []
    
    class Config:
        orm_mode = True