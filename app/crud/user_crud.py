from sqlalchemy.orm import Session
from schemas.schemas import BaseUser,LogIn
from models.models import User
import bcrypt
from fastapi import HTTPException,status
from middleware.auth_service import create_access_token 

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



def read_user_info(login_data:LogIn,db:Session):
    
    db_user=db.query(User).filter(User.email == login_data.email).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    if not bcrypt.checkpw(login_data.password.encode(), db_user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "password is wrong")


    token = create_access_token(user_id = db_user.id,role = db_user.role)
    return {"message":"you log in your account ", "role":db_user.role, "access_token":token }



def read_user(db:Session, user_id : int):
    pass