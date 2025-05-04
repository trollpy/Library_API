from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None


class AuthorResponse(AuthorBase):
    author_id: int
    
    class Config:
        orm_mode = True