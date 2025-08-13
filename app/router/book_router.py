
from fastapi import UploadFile,File,Form,APIRouter,Query,Depends,status,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.schemas import SearchBook,UploudBook,DeleteMessageBook,UpdateMessageBook
from models.models import Book 
from typing import Optional,Annotated
from middleware.auth_service import get_current_user
from crud import book_crud
from typing import Optional


file_router=APIRouter(prefix = "/file")

@file_router.post("/upload", response_model = UploudBook, status_code = status.HTTP_201_CREATED)
def uploud_book(
                title:str = Form(...), publisher:str = Form(...),
                author:str = Form(...), page_count:int = Form(...),
                pdf:UploadFile = File(...),img:UploadFile = File(...),
                db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    return book_crud.uploud_book_info(
        title = title, publisher = publisher,
        author = author ,page_count = page_count,
        pdf = pdf, img = img, 
        db = db, current_user = current_user)
    




@file_router.get("/search",response_model = SearchBook, status_code = status.HTTP_200_OK)
def search_book(
    id:int = Query(ge = 1),db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)):

    return book_crud.search_book_info(id=id, db=db, current_user=current_user)
   
   
       
   


@file_router.delete("/delete",response_model = DeleteMessageBook, status_code = status.HTTP_200_OK)
def delete_book(
    id:int = Query(ge=1), db:Session = Depends(get_db), 
    current_user:dict = Depends(get_current_user)):

    return book_crud.delete_book_info(id=id, db=db, current_user=current_user)
    
    



@file_router.patch("/update",response_model = UpdateMessageBook,status_code = status.HTTP_200_OK)
def update_book(
                id: int = Form(...),title:Optional[str]=Form(None),
                publisher:Optional[str] = Form(None), author:Optional[str] = Form(None),
                page_count:Optional[str] = Form(None), pdf: Annotated[UploadFile | str, File()] = None, 
                db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    return book_crud.update_book_info(
        id=id,title = title, publisher = publisher,
        author = author ,page_count = page_count,
        pdf = pdf, db = db, current_user = current_user)
    
   

    
    
    
  

