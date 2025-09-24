from sqlalchemy import Boolean, String, Integer, DateTime, Column, ForeignKey, Text, Index, UniqueConstraint, CheckConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database import Base


class UserEmail(Base):
    __tablename__ = "user_emails"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    code = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    user = relationship("User", back_populates="user_email")  

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
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    user_email_id = Column(Integer, ForeignKey("user_emails.id", ondelete="CASCADE"), nullable=False)

    user_email = relationship("UserEmail", back_populates="user")
    products = relationship("Product", back_populates="user")


class TypeProduct(Base):
    __tablename__ = "type_products"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)

    products = relationship("Product", back_populates="type_product")


class Photo(Base):  
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(Text, nullable=False)

    product_photos = relationship("ProductPhoto", back_populates="photo")


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True, index=True)

    subcategories = relationship("ProductSubCategory", back_populates="category")


class ProductSubCategory(Base):
    __tablename__ = "product_subcategories"

    id = Column(Integer, primary_key=True)
    subcategory_name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)

    category = relationship("ProductCategory", back_populates="subcategories")
    subsubcategories = relationship("ProductSubSubCategory", back_populates="subcategory")


class ProductSubSubCategory(Base):
    __tablename__ = "product_subsubcategories"

    id = Column(Integer, primary_key=True)
    sub_subcategory_name = Column(String, index=True)
    subcategory_id = Column(Integer, ForeignKey("product_subcategories.id"), nullable=False)

    subcategory = relationship("ProductSubCategory", back_populates="subsubcategories")

    products = relationship("Product",foreign_keys="Product.product_subsubcategory_id",back_populates="subsubcategory")

    exchange_products = relationship("Product",foreign_keys="Product.exchange_item_subsubcategory_id",back_populates="exchange_item_subsubcategory")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    exchange_item = Column(Text, nullable=False)
    product_subsubcategory_id = Column(Integer, ForeignKey("product_subsubcategories.id"), nullable=False)
    exchange_item_subsubcategory_id = Column(Integer, ForeignKey("product_subsubcategories.id"), nullable=False)
    type_product_id = Column(Integer, ForeignKey("type_products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())

    subsubcategory = relationship("ProductSubSubCategory", foreign_keys=[product_subsubcategory_id], back_populates="products")
    exchange_item_subsubcategory = relationship("ProductSubSubCategory", foreign_keys=[exchange_item_subsubcategory_id], back_populates="exchange_products")
    type_product = relationship("TypeProduct", back_populates="products")
    user = relationship("User", back_populates="products")
    product_photos = relationship("ProductPhoto", back_populates="product")  
    related_products_1 = relationship("RelatedProduct", foreign_keys="RelatedProduct.product_id_1", back_populates="product_1")
    related_products_2 = relationship("RelatedProduct", foreign_keys="RelatedProduct.product_id_2", back_populates="product_2")


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)

    product = relationship("Product", back_populates="product_photos")
    photo = relationship("Photo", back_populates="product_photos")


class RelatedProduct(Base):
    __tablename__ = "related_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id_1 = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product_id_2 = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    product_1 = relationship("Product", foreign_keys=[product_id_1], back_populates="related_products_1")
    product_2 = relationship("Product", foreign_keys=[product_id_2], back_populates="related_products_2")

    __table_args__ = (
        UniqueConstraint('product_id_1', 'product_id_2', name='uq_related_products'),
        Index('ix_related_products_product_ids', 'product_id_1', 'product_id_2'),
        CheckConstraint('product_id_1 != product_id_2', name='ck_different_products')
    )