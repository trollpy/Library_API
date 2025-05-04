from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Table
from sqlalchemy.orm import relationship

from app.database import Base


# Association table for the many-to-many relationship between books and authors
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.book_id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.author_id"), primary_key=True)
)


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String(150), nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="books")
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    loans = relationship("Loan", back_populates="book")