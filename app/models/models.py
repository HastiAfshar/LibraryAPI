from sqlalchemy import Column, Integer, String, VARCHAR, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username =Column(VARCHAR(40), nullable=False, unique=True)
    email = Column(VARCHAR(50),nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at =Column ( TIMESTAMP,nullable=False,server_default=func.now())
    updated_at = Column ( TIMESTAMP,nullable=False,server_default=func.now())
