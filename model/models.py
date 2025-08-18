from sqlalchemy import Boolean, String, Integer, DateTime, Column, ForeignKey, Text, Index, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database import Base


class UserEmail(Base):
    __tablename__ = "user_emails"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    code = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="user_email")

    __table_args__ = (
        UniqueConstraint('email', name='uq_user_emails_email'),
        Index('ix_user_emails_code', 'code'),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=True, default="")
    phone_number = Column(String(20), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_email_id = Column(Integer, ForeignKey("user_emails.id", ondelete="CASCADE"), nullable=False)

    user_email = relationship("UserEmail", back_populates="users")


class TypeProduct(Base):
    __tablename__ = "type_products"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(Text, nullable=False)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)

    product_subcategoies = relationship("ProductSubCategory", back_populates="product_category")


class ProductSubCategory(Base):
    __tablename__ = "product_subcategories"

    id = Column(Integer, primary_key=True, index=True)
    subcategory_name = Column(String, nullable=False)

    product_category_id = Column(Integer, ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False)

    product_category = relationship("ProductCategory", back_populates="product_subcategories")
    product_sub_subcategories = relationship("ProductSubSubCategory", back_populates="product_subcategory")


class ProductSubSubCategory(Base):
    __tablename__ = "product_sub_subcategories"

    id = Column(Integer, primary_key=True, index=True)
    sub_subcategory_name = Column(String, nullable=False)

    product_subcategory_id = Column(Integer, ForeignKey("product_subcategories.id", ondelete="CASCADE"), nullable=False)

    product_subcategory = relationship("ProductSubCategory", back_populates="product_sub_subcategories")


# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     product_name = Column(String, nullable=False)
