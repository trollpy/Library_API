from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(
    prefix="/members",
    tags=["members"],
    responses={404: {"description": "Member not found"}}
)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    # Check if member with email already exists
    existing_member = db.query(Member).filter(Member.email == member.email).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member with this email already exists"
        )
    
    db_member = Member(
        first_name=member.first_name,
        last_name=member.last_name,
        email=member.email,
        phone=member.phone,
        address=member.address
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=List[MemberResponse])
def read_members(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Member)
    
    # Apply filters if provided
    if name:
        query = query.filter(
            (Member.first_name.ilike(f"%{name}%")) | 
            (Member.last_name.ilike(f"%{name}%"))
        )
    if status:
        query = query.filter(Member.membership_status == status)
    
    members = query.offset(skip).limit(limit).all()
    return members


@router.get("/{member_id}", response_model=MemberResponse)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.member_id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.member_id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if updating email to one that already exists
    if member.email and member.email != db_member.email:
        existing_member = db.query(Member).filter(Member.email == member.email).first()
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member with this email already exists"
            )
    
    update_data = member.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_member, key, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.member_id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(db_member)
    db.commit()
    return None