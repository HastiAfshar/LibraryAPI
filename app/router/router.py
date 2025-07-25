from fastapi import APIRouter,Depends,HTTPException,status,Path,Query,UploadFile,File,Form
from models.models import Base,User
from schemas.schemas import BaseUser,SignupResponse,UserUpdateResponse,SearchUserResponse,UserDeleteResponse
from sqlalchemy.orm import Session
from db import get_db,engine
import bcrypt
from typing import List,Optional

router=APIRouter(prefix="/auth")

user_router=APIRouter(prefix="/user")

Base.metadata.create_all(bind=engine)


@router.get("/")
def welcome() -> str:
    
    return "welcome"


@router.post(path="/signup",response_model=SignupResponse,status_code=status.HTTP_201_CREATED)
def create_user(user_data:BaseUser,db:Session=Depends(get_db)):
     if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email already exist")
    
     new_user = User(username=user_data.username,email=user_data.email)
     hashed_password = bcrypt.hashpw(password=user_data.password.encode(),salt=bcrypt.gensalt())
     new_user.password = hashed_password

     db.add(new_user)
     db.commit()
     return {"message":"new user created","user_id":new_user.id,"username":new_user.username}



@user_router.get(path="/read/{user_id}",response_model=None,status_code=status.HTTP_200_OK)
def read_user(user_id:int=Path(ge=1),db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with {user_id} not found")
    return db_user



@user_router.patch("/update/{user_id}",response_model=UserUpdateResponse,status_code=status.HTTP_200_OK)
def update_user(user_data:BaseUser,user_id: int = Path(ge=1) ,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with {user_id} not found")
    else:
        db_user.username = user_data.username
        db_user.email = user_data.email
        db_user.password = user_data.password
    

    db.commit()

    return {"message":"user updated","user_id":db_user.id,}


@user_router.delete("/delete/{user_id}",response_model=UserDeleteResponse,status_code=status.HTTP_200_OK)
def delete_user(user_id:int=Path(ge=1),db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user with {user_id} not found")

    db.delete(db_user)
    db.commit()

    return {"message":"user deleted","user_id":db_user.id}


@user_router.get("/search/",response_model=List[SearchUserResponse],status_code=status.HTTP_200_OK)
def search_user(start : int = Query(1,ge=1),end:int = Query(100,le=1000),db:Session=Depends(get_db)):
    
    db_user = db.query(User).filter(User.id >= start,User.id <= end ).all()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="users not found")
    return db_user


