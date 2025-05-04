from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    membership_status: Optional[str] = None


class MemberResponse(MemberBase):
    member_id: int
    membership_date: date
    membership_status: str
    
    class Config:
        orm_mode = True