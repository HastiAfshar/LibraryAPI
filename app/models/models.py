from sqlalchemy import Column, Integer, String, VARCHAR, TIMESTAMP, func ,ForeignKey,LargeBinary
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120),unique=True , nullable=False)
    username = Column(String(120), nullable=False)
    password = Column(LargeBinary(1500), nullable=False)
    created_at = Column(TIMESTAMP,server_default=func.now() ,nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(),nullable=False)
    
    
    books = relationship('Book',back_populates='user',cascade='all, delete',passive_deletes=True)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    publisher = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    page_count = Column(Integer,nullable=False)
    download_url = Column(String(2000),nullable=False)  
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now() ,nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now() ,nullable=False)

    user = relationship('User', back_populates='books')

