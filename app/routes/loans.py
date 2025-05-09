from typing import List, Optional
from datetime import date, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.loan import Loan
from app.models.book import Book
from app.models.member import Member
from app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
    responses={404: {"description": "Loan not found"}}
)


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Check if book exists and is available
    book = db.query(Book).filter(Book.book_id == loan.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    if book.available_copies <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available for loan"
        )
    
    # Check if member exists and is active
    member = db.query(Member).filter(Member.member_id == loan.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    if member.membership_status != 'active':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member's status is {member.membership_status}, not active"
        )
    
    # Create loan
    db_loan = Loan(
        book_id=loan.book_id,
        member_id=loan.member_id,
        due_date=loan.due_date,
        status='borrowed'
    )
    
    # Update book's available copies
    book.available_copies -= 1
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


@router.get("/", response_model=List[LoanResponse])
def read_loans(
    skip: int = 0, 
    limit: int = 100,
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Loan)
    
    # Apply filters if provided
    if member_id:
        query = query.filter(Loan.member_id == member_id)
    if book_id:
        query = query.filter(Loan.book_id == book_id)
    if status:
        query = query.filter(Loan.status == status)
    
    loans = query.options(
        joinedload(Loan.book),
        joinedload(Loan.member)
    ).offset(skip).limit(limit).all()
    
    return loans


@router.get("/{loan_id}", response_model=LoanResponse)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: int, loan: LoanUpdate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    update_data = loan.dict(exclude_unset=True)
    
    # If returning a book, update book availability
    if update_data.get('status') == 'returned' and db_loan.status != 'returned':
        # Mark as returned
        db_loan.return_date = date.today() if not update_data.get('return_date') else update_data['return_date']
        
        # Update book's available copies
        book = db.query(Book).filter(Book.book_id == db_loan.book_id).first()
        if book:
            book.available_copies += 1
        
        # Calculate fine if returned late
        if db_loan.due_date < db_loan.return_date:
            days_late = (db_loan.return_date - db_loan.due_date).days
            fine_per_day = Decimal('0.50')  # $0.50 per day
            db_loan.fine_amount = days_late * fine_per_day
    
    for key, value in update_data.items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    return db_loan


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # If the loan is borrowed, increase the book's available copies when deleted
    if db_loan.status == 'borrowed':
        book = db.query(Book).filter(Book.book_id == db_loan.book_id).first()
        if book:
            book.available_copies += 1
    
    db.delete(db_loan)
    db.commit()
    return None


@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """Convenience endpoint to return a book"""
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if db_loan.status == 'returned':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book has already been returned"
        )
    
    return_date = date.today()
    db_loan.return_date = return_date
    db_loan.status = 'returned'
    
    # Update book's available copies
    book = db.query(Book).filter(Book.book_id == db_loan.book_id).first()
    if book:
        book.available_copies += 1
    
    # Calculate fine if returned late
    if db_loan.due_date < return_date:
        days_late = (return_date - db_loan.due_date).days
        fine_per_day = Decimal('0.50')  # $0.50 per day
        db_loan.fine_amount = days_late * fine_per_day
    
    db.commit()
    db.refresh(db_loan)
    return db_loan