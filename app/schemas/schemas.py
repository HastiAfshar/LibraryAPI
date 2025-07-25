from pydantic import BaseModel,EmailStr



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