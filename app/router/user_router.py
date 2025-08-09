from fastapi import APIRouter,Depends,HTTPException,status,Path,Query
from models.models import Base,User
from schemas.schemas import BaseUser,SignupResponse,UserUpdateResponse,SearchUserResponse,UserDeleteResponse,ReadUserResponse,LogIn,LogInResponse
from sqlalchemy.orm import Session
from db import get_db
import bcrypt
from typing import List
from middleware.auth_service import create_access_token , get_current_user


router=APIRouter(prefix="/auth")

user_router=APIRouter(prefix="/user")


@router.post(path = "/signup",response_model = SignupResponse,status_code = status.HTTP_201_CREATED )
def create_user(user_data:BaseUser, db:Session = Depends(get_db)):
     
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

     
     return {"message":"new user created","user_id":new_user.id,"username":new_user.username,"role":new_user.role}

@router.post("/login",response_model=LogInResponse)
def login(login_data:LogIn,db:Session=Depends(get_db)):
    
    db_user=db.query(User).filter(User.email == login_data.email).first()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    if not bcrypt.checkpw(login_data.password.encode(), db_user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "password is wrong")


    token = create_access_token(user_id = db_user.id,role = db_user.role)
    return {"message":"you log in your account ", "role":db_user.role, "access_token":token }


@user_router.get(path="/read/{user_id}", response_model = ReadUserResponse,status_code = status.HTTP_200_OK)
def read_user(
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id==current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"user with not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't update user data :|")
   
    return {"username":db_user.username,"id":db_user.id,"email":db_user.email}
    
    


@user_router.patch("/update/{user_id}",response_model=UserUpdateResponse,status_code=status.HTTP_200_OK)
def update_user(
                user_data:BaseUser,
                db:Session = Depends(get_db),
                current_user:dict = Depends(get_current_user)):
    
    
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

    return {"message":"user updated","user_id":db_user.id,}


@user_router.delete("/delete/{user_id}",response_model=UserDeleteResponse,status_code=status.HTTP_200_OK)
def delete_user(db:Session = Depends(get_db),current_user:dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id==current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user with {user_id} not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't delete user data")

    db.delete(db_user)
    db.commit()

    return {"message":"user deleted","user_id":db_user.id}


@user_router.get("/search/", response_model = List[SearchUserResponse], status_code = status.HTTP_200_OK)
def search_user(
    start:int = Query(1,ge=1), end:int = Query(100,le=1000), 
    db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id >= start,User.id <= end ).all()
    
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "users not found")
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't search users")

    
    return db_user



