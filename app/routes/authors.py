from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    responses={404: {"description": "Author not found"}}
)


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(
        first_name=author.first_name,
        last_name=author.last_name,
        birth_date=author.birth_date,
        nationality=author.nationality,
        biography=author.biography
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/", response_model=List[AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    update_data = author.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)
    
    db.commit()
    db.refresh(db_author)
    return db_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    return None