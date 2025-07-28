from fastapi import HTTPException
from dotenv  import load_dotenv
import os
import boto3


load_dotenv()

LIARA_ENDPOINT=os.getenv("LIARA_ENDPOINT")
LIARA_BUCKET_NAME=os.getenv("LIARA_BUCKET_NAME")
LIARA_ACCESS_KEY=os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY=os.getenv("LIARA_SECRET_KEY")

print(LIARA_ENDPOINT)


s3=boto3.client("s3",endpoint_url=LIARA_ENDPOINT,aws_access_key_id=LIARA_ACCESS_KEY,aws_secret_access_key=LIARA_SECRET_KEY)

def upload_file(file, file_name):
    try:
        s3.upload_fileobj(file.file, LIARA_BUCKET_NAME, file_name)
        return f"{LIARA_ENDPOINT}/{LIARA_BUCKET_NAME}/{file_name}"
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error uploading file: {e}")
    


def delete_file(bucket_name:str, file_name:str):
    try:
        s3.delete_object(Bucket=bucket_name,Key=file_name)
        return f"File '{file_name}' deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error deleting file: {e}")





if __name__ =="__main__":
    with open (file="book_test.pdf",mode="rb") as file:
        link=upload_file(file=file,file_name="book_test2.pdf")
        print(link)