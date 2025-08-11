from sqlalchemy.orm import Session
from schemas.schemas import BaseUser
from models.models import User
import bcrypt
from fastapi import HTTPException,status

def create_user(user_data:BaseUser, db:Session):
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exist")
    
    db_count= db.query(User).count()
    if db_count == 0:
        role = "admin"
    else: 
        role = "user"

     
    new_user = User(username = user_data.username, email = user_data.email, role = role)
    hashed_password = bcrypt.hashpw(password = user_data.password.encode(), salt = bcrypt.gensalt())
    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

     
    return {
        "message":"new user created",
        "user_id":new_user.id, 
        "username":new_user.username,
        "role":new_user.role}

def read_user(db:Session, user_id : int):
    pass