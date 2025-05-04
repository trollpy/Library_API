from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String(100), nullable=True)
    biography = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    books = relationship("Book", secondary="book_authors", back_populates="authors")