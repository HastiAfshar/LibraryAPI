from fastapi import UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from middleware.bucket import upload_file,delete_file,LIARA_BUCKET_NAME
from models.models import Book 
from typing import Optional



def uploud_book_info(
                title:str , publisher:str,
                author:str , page_count:int ,
                pdf:UploadFile ,img:UploadFile ,
                db:Session , current_user:dict):
    
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


def search_book_info( id:int, db:Session, current_user:Optional[dict]):

    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found")
   
    if current_user is None:
       return {
           "id":db_book.id, "title":db_book.title, 
           "publisher":db_book.publisher,"author":db_book.author,
           "page_count":db_book.page_count}
   
    return {
           "id":db_book.id, "title":db_book.title,
            "publisher":db_book.publisher,"author":db_book.author,
            "page_count":db_book.page_count,"downloud_url":db_book.download_url}




def delete_book_info(id:int, db:Session , current_user:dict ):
    
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



def update_book_info(
                id: int, title:Optional[str] ,
                publisher:Optional[str] , author:Optional[str],
                page_count:Optional[str] , pdf:str, 
                db:Session, current_user:dict ):
     
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