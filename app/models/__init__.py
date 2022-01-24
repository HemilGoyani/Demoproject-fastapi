import enum
from pydantic import BaseModel
from app.database.db import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.orm import relationship
from app.database.db import Base
from sqlalchemy.types import Enum

 

    
class Usersignup(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    address = Column(String,index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String,index=True)
    
    user = relationship('UserRole', back_populates='user')
    roles = relationship('Role', back_populates='user')
    permissions = relationship('Permission',back_populates='user')

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

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(100))
    active = Column(Boolean, default=True)
    
    permissions = relationship('Permission', back_populates='roles')
    user_role = relationship("UserRole", back_populates="role")
    

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    user = relationship('Usersignup',back_populates='user')
    role = relationship("Role", back_populates="user_role")
   
class Modules(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    permission = relationship("Permission", back_populates="module")

class AccessName(enum.Enum):
    READ = "READ"
    READ_WRITE = "READ_WRITE"
    
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_type = Column(Enum(AccessName))
    role_id = Column(Integer, ForeignKey(Role.id))
    module_id = Column(Integer, ForeignKey(Modules.id))

    user = relationship('Usersignup', back_populates='permissions')
    roles = relationship("Role", back_populates='permissions')
    module = relationship("Modules", back_populates="permission")
    

   
