from sqlalchemy import Boolean, String, Integer, DateTime, Column, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database import Base


class UserEmail(Base):
    __tablename__ = "user_emails"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    code = Column(Integer, nullable=True)

    users = relationship("User", back_populates="user_email")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=True, default="")
    phone_number = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_email = Column(Integer, ForeignKey("user_emails.id", ondelete="CASCADE"), nullable=False)

    user_email = relationship("UserEmail", back_populates="users")