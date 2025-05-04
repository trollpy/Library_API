from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.database import Base


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.member_id"), nullable=False)
    loan_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(
        Enum('borrowed', 'returned', 'overdue', name='loan_status'),
        default='borrowed',
        nullable=False
    )
    fine_amount = Column(DECIMAL(10, 2), default=0.00, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")