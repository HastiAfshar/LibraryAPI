from pydantic import BaseModel,EmailStr




class BaseUser(BaseModel):
    username:str
    email:EmailStr
    password:str
    

class SignupResponse(BaseModel):
    message:str
    user_id:int
    username:str
    role:str
    

class LogIn(BaseModel):
    email:EmailStr
    password:str

class LogInResponse(BaseModel):
    message:str
    role:str
    access_token:str


class ReadUserResponse(BaseModel):
    username : str
    id:int
    email:EmailStr


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


class UploudBook(BaseModel):
    message:str
    book_id:int
    pdf_url:str
    img_url:str


class SearchBook(BaseModel):
    id: int
    title:str
    publisher:str
    author:str
    page_count:int
    downloud_url:str


class DeleteMessageBook(BaseModel):
    message:str 


class UpdateMessageBook(BaseModel):
    message:str 
   


    
