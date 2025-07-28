from pydantic import BaseModel,EmailStr
from typing import Optional



class BaseUser(BaseModel):
    username:str
    email:EmailStr
    password:str



class SignupResponse(BaseModel):
    message:str
    user_id:int
    username:str


class UserUpdateResponse(BaseModel):
    message:str
    user_id:int

class UserDeleteResponse(BaseModel):
    message:str
    user_id: int
    
class SearchUserResponse(BaseModel):
    username : str
    id:int
    email:EmailStr


class BookUpdate(BaseModel):
    id: int
    title:Optional[str] = None
    publisher:Optional[str] = None
    author:Optional[str] = None
    page_count:Optional[int] = None
    user_id:Optional[int] = None
    
