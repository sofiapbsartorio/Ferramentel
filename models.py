from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    address = Column(String)
    cpf = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)
    is_manager = Column(Boolean, default=False)

class Tool(Base):
    __tablename__ = 'tools'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    available = Column(Boolean, default=True)

class Rental(Base):
    __tablename__ = 'rentals'
    
    id = Column(Integer, primary_key=True, index=True)
    request_date = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(DateTime)
    return_date = Column(DateTime)
    status = Column(String, default="em análise")
    client_id = Column(Integer, ForeignKey('users.id'))
    manager_id = Column(Integer, ForeignKey('users.id'))
    tool_id = Column(Integer, ForeignKey('tools.id'))
    
    client = relationship("User", foreign_keys=[client_id])
    manager = relationship("User", foreign_keys=[manager_id])
    tool = relationship("Tool")
