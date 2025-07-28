from middleware.bucket import upload_file,delete_file,LIARA_BUCKET_NAME
from fastapi import UploadFile,File,Form,APIRouter,Query,Depends,status,HTTPException
from sqlalchemy.orm import Session
from db import get_db,engine
import bcrypt
from models.models import Book
from typing import Optional
from schemas.schemas import BookUpdate

file_router=APIRouter(prefix="/file")

@file_router.post("/upload",status_code=status.HTTP_201_CREATED)
def uploud_book(title:str=Form(...),publisher:str=Form(...),author:str=Form(...),page_count:int=Form(...),user_id:int=Form(...),pdf:UploadFile=File(...),db:Session=Depends(get_db)):

    pdf_url=upload_file(pdf,f"test/{title}.pdf")
    

    new_book = Book(title=title,publisher=publisher,author=author,page_count=page_count, download_url=pdf_url,user_id=user_id )
    
    db.add(new_book)
    db.commit()
    return {"message":"file created","Book_id":new_book.id,"pdf_url":pdf_url}




@file_router.get("/search",status_code=status.HTTP_200_OK)
def search_book(id:int=Query(ge=1),db:Session=Depends(get_db)):
   db_book = db.query(Book).filter(Book.id == id).first()
   if not db_book:
        raise HTTPException(status_code=404,detail=f"book not found")

   return db_book


@file_router.delete("/delete",status_code=status.HTTP_200_OK)
def delete_book(id:int=Query(ge=1),db:Session=Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404,detail=f"book not found")
    key=f"test/{db_book.title}.pdf"
    delete_file(bucket_name=LIARA_BUCKET_NAME,file_name=key)
    

    db.delete(db_book)
    db.commit()
    return {"message":"book deleted"}


@file_router.patch("/update",status_code=status.HTTP_200_OK)
def uploud_book(book_data:BookUpdate = Depends(),pdf:Optional[UploadFile]=File(None),db:Session=Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_data.id).first()
    if not db_book:
        raise HTTPException(status_code=404,detail=f"book not found")
    else :
        old_title = db_book.title
        if book_data.title:
            db_book.title = book_data.title
    
        if book_data.publisher:
            db_book.publisher = book_data.publisher
    
        if book_data.author:
            db_book.author = book_data.author

        if book_data.page_count:
            db_book.page_count = book_data.page_count

        if book_data.user_id:
            db_book.user_id = book_data.user_id
    
        if pdf:
            old_key=f"test/{old_title}.pdf"
            delete_file(bucket_name=LIARA_BUCKET_NAME,file_name=old_key)
            
            new_url=upload_file(pdf,f"test/{db_book.title}.pdf")
            db_book.download_url=new_url
  
        db.commit()
        db.refresh(db_book)

        return {"message":"book updated"}

    
    
    
  

