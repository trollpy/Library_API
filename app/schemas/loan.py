from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel

from app.schemas.book import BookResponse
from app.schemas.member import MemberResponse


class LoanBase(BaseModel):
    book_id: int
    member_id: int
    due_date: date


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    status: Optional[str] = None
    fine_amount: Optional[Decimal] = None


class LoanResponse(LoanBase):
    loan_id: int
    loan_date: date
    return_date: Optional[date] = None
    status: str
    fine_amount: Decimal
    book: Optional[BookResponse] = None
    member: Optional[MemberResponse] = None
    
    class Config:
        orm_mode = True