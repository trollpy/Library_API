from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookUpdate, BookResponse

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Book not found"}}
)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Create new book
    db_book = Book(
        title=book.title,
        isbn=book.isbn,
        publication_year=book.publication_year,
        publisher=book.publisher,
        total_copies=book.total_copies,
        available_copies=book.total_copies,
        category_id=book.category_id
    )
    
    # Add authors
    for author_id in book.author_ids:
        author = db.query(Author).filter(Author.author_id == author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        db_book.authors.append(author)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[BookResponse])
def read_books(
    skip: int = 0, 
    limit: int = 100, 
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    
    # Apply filters if provided
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author_id:
        query = query.filter(Book.authors.any(Author.author_id == author_id))
    if category_id:
        query = query.filter(Book.category_id == category_id)
    
    books = query.offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update book attributes
    update_data = book.dict(exclude={"author_ids"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    # Update authors if provided
    if book.author_ids is not None:
        # Clear current authors
        db_book.authors = []
        
        # Add new authors
        for author_id in book.author_ids:
            author = db.query(Author).filter(Author.author_id == author_id).first()
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Author with ID {author_id} not found"
                )
            db_book.authors.append(author)
    
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return None