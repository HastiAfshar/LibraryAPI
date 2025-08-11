from pydantic import BaseModel,EmailStr,field_validator,Field
import re




class BaseUser(BaseModel):
    username:str = Field(min_length=3,max_length=35)
    email:EmailStr
    password:str
    


    @field_validator("username")
    @classmethod  
    def validate_username(cls, value:str) -> str:
        if not re.match(r"^[A-Za-z0-9_]",value):
            raise ValueError("username can only contain letters")
        return value
    
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value:str) -> str:
        if re.match(r"^(?=.*[A-Za-z])(?=.*\d).+$",value):
            raise ValueError("password must contain  letter and number")
        return value


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
   


    
