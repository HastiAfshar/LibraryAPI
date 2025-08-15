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



def read_login_info(login_data:LogIn,db:Session):

    db_user=db.query(User).filter(User.email == login_data.email).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    if not bcrypt.checkpw(login_data.password.encode(), db_user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "password is wrong")


    token = create_access_token(user_id = db_user.id,role = db_user.role)
    return {"message":"you log in your account ", "role":db_user.role, "access_token":token }



def read_user_info( current_user:dict, db:Session):
    db_user = db.query(User).filter(User.id==current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"user with not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't update user data :|")
   
    return {"username":db_user.username,"id":db_user.id,"email":db_user.email}



def update_user_info(user_data:BaseUser,db:Session ,current_user:dict):

    db_user=db.query(User).filter(User.id==current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "user with {user_id} not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't update user data :|")
    
    else:
        db_user.username = user_data.username
        db_user.email = user_data.email
        hashed_password = bcrypt.hashpw(password = user_data.password.encode(), salt = bcrypt.gensalt())
        db_user.password = hashed_password
    

    db.commit()

    return {"message":"user updated","user_id":db_user.id}


def delete_user_info(current_user:dict ,db:Session):
    db_user = db.query(User).filter(User.id==current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user with {user_id} not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't delete user data")
    
    db.query(User).filter(User.id== db_user.id).update({"delete_account":True})
    
    db.commit()

    
    return {"message":"user deleted","user_id":db_user.id}


def search_user_info(start:int, end:int, db:Session, current_user:dict):

    db_user = db.query(User).filter(User.id >= start,User.id <= end ).all()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "users not found")
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't search users")

    
    return db_user