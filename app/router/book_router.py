from middleware.bucket import upload_file,delete_file,LIARA_BUCKET_NAME
from fastapi import UploadFile,File,Form,APIRouter,Query,Depends,status,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from app.schemas.response_schemas import SearchBook,UploudBook,DeleteMessageBook,UpdateMessageBook
from models.models import Book 
from typing import Optional,Annotated
from middleware.auth_service import get_current_user

file_router=APIRouter(prefix = "/file")

@file_router.post("/upload", response_model = UploudBook, status_code = status.HTTP_201_CREATED)
def uploud_book(
                title:str = Form(...), publisher:str = Form(...),
                author:str = Form(...), page_count:int = Form(...),
                pdf:UploadFile = File(...),img:UploadFile = File(...),
                db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    

    pdf_url=upload_file(pdf,f"test/{title}.pdf")
    img_url=upload_file(img,f"test/{title}.png")

    
    new_book = Book(
                    title = title,publisher = publisher,
                    author = author,page_count = page_count,
                    download_url = pdf_url , user_id = current_user["user_id"])
    
    if current_user["role"] != "admin" and current_user["user_id"] != new_book.user_id : 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't uploud book and  image:|")
    
    db.add(new_book)
    db.commit()
    return {"message":"file created", "book_id":new_book.id, "pdf_url":pdf_url, "img_url":img_url}




@file_router.get("/search",response_model = SearchBook, status_code = status.HTTP_200_OK)
def search_book(
    id:int = Query(ge = 1),db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)):
   
   db_book = db.query(Book).filter(Book.id == id).first()
   


@file_router.delete("/delete",response_model = DeleteMessageBook, status_code = status.HTTP_200_OK)
def delete_book(
    id:int = Query(ge=1), db:Session = Depends(get_db), 
    current_user:dict = Depends(get_current_user)):
    

    db_book = db.query(Book).filter(Book.id == id).first()
    
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_book.user_id : 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't delete book ")
    
    key=f"test/{db_book.title}.pdf"
    delete_file(bucket_name = LIARA_BUCKET_NAME, file_name = key)
    

    db.delete(db_book)
    db.commit()
    return {"message":"book deleted"}


@file_router.patch("/update",response_model = UpdateMessageBook,status_code = status.HTTP_200_OK)
def update_book(
                id: int = Form(...),title:Optional[str]=Form(None),
                publisher:Optional[str] = Form(None), author:Optional[str] = Form(None),
                page_count:Optional[str] = Form(None), pdf: Annotated[UploadFile | str, File()] = None, 
                db:Session = Depends(get_db), current_user:dict = Depends(get_current_user)):
    
    db_book = db.query(Book).filter(Book.id == id).first()
    
    if not db_book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"book not found")
    
    if current_user["role"] != "admin" and current_user["user_id"] != db_book.user_id : 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "you can't update book ")
    
    old_title = db_book.title
    if title:
        db_book.title =title
           
    if publisher:
        db_book.publisher = publisher
            
    if author:
        db_book.author = author

    if page_count:
        db_book.page_count = page_count


    
    if pdf:
        old_key=f"test/{old_title}.pdf"
        delete_file(bucket_name = LIARA_BUCKET_NAME, file_name = old_key)
        
            
        new_url=upload_file(pdf, f"test/{db_book.title}.pdf")
        db_book.download_url = new_url
  

       
        
  
    db.commit()
    db.refresh(db_book)

    return {"message":"book updated"}

    
    
    
  

