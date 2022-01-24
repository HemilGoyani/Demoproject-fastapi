from app.database.db import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.orm import relationship
from app.database.db import Base

class Usersignup(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    address = Column(String,index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String,index=True)
    

class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    
    products = relationship(
        "Product", back_populates="brand")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    name = Column(String, index=True)
    active = Column(Boolean, default=True)

    brand = relationship("Brand", back_populates="products")