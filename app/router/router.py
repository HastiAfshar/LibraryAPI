from fastapi import APIRouter,Depends,HTTPException
from models.models import Base,User
from schemas.schemas import BaseUser
from sqlalchemy.orm import Session
from db import get_db,engine

router=APIRouter()

Base.metadata.create_all(bind=engine)


@router.get("/")
def welcome() -> str:
    
    return "welcome"




@router.post("/users_register")
def user_register(user_credentials=BaseUser , db:Session=(Depends(get_db))):
    if db.query(User).filter(User.email == user_credentials.email):
        raise HTTPException(status_code=409,detail="email already exist")
    
    new_user=User(username=user_credentials.username,email=user_credentials.email,password=user_credentials.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return User(usernaame=new_user.username,email=new_user.email,message="User registed succcessfully")

