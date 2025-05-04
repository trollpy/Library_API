from sqlalchemy import Column, Integer, String, Text, Date, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    membership_date = Column(Date, nullable=False, server_default=func.current_date())
    membership_status = Column(
        Enum('active', 'expired', 'suspended', name='membership_status'),
        default='active',
        nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    loans = relationship("Loan", back_populates="member")