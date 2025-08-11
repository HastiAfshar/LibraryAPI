from fastapi import APIRouter,Depends,HTTPException,status,Path,Query
from models.models import User
from schemas.schemas import BaseUser,SignupResponse,UserUpdateResponse,SearchUserResponse,UserDeleteResponse,ReadUserResponse,LogIn,LogInResponse
from sqlalchemy.orm import Session
from db import get_db
import bcrypt
from typing import List
from middleware.auth_service import create_access_token , get_current_user
from crud import user_crud

router=APIRouter(prefix="/auth")
user_router=APIRouter(prefix="/user")


@router.post(path = "/signup",response_model = SignupResponse,status_code = status.HTTP_201_CREATED )
def signup_user(user_data:BaseUser, db:Session = Depends(get_db)):
    
    return user_crud.create_user(user_data=user_data,db=db)

     
    
@router.post("/login",response_model=LogInResponse)
def login(login_data:LogIn,db:Session=Depends(get_db)):
    
    return user_crud.read_login_info(login_data=login_data,db=db)
    
    


@user_router.get(path="/read/{user_id}", response_model = ReadUserResponse,status_code = status.HTTP_200_OK)
def read_user(db:Session = Depends(get_db),current_user:dict = Depends(get_current_user)):
    
    return user_crud.read_user_info(current_user=current_user,db=db)
    
    


@user_router.patch("/update/{user_id}",response_model=UserUpdateResponse,status_code=status.HTTP_200_OK)
def update_user(user_data:BaseUser,db:Session = Depends(get_db),current_user:dict = Depends(get_current_user)):
    
     return user_crud.update_user_info(user_data = user_data, db = db, current_user = current_user)


@user_router.delete("/delete/{user_id}",response_model=UserDeleteResponse,status_code=status.HTTP_200_OK)
def delete_user(db:Session = Depends(get_db),current_user:dict = Depends(get_current_user)):
    
    return user_crud.delete_user_info(current_user=current_user,db=db)
    
    


@user_router.get("/search/", response_model = List[SearchUserResponse], status_code = status.HTTP_200_OK)
def search_user(
    start:int = Query(1,ge=1), end:int = Query(100,le=1000), 
    db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    return user_crud.search_user_info(start = start, end = end, db = db, current_user=current_user)



