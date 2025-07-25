from fastapi import APIRouter,File,UploadFile
from typing import Optional,List
from urllib.parse import quote
from dotenv  import load_dotenv
import os
import boto3
from botocore.exceptions import NoCredentialsError,PartialCredentialsError
import streamlit as st


load_dotenv()

LIARA_ENDPOINT=os.getenv("LIARA_ENDPOINT")
LIARA_BUCKET_NAME=os.getenv("LIARA_BUCKET_NAME")
LIARA_ACCESS_KEY=os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY=os.getenv("LIARA_SECRET_KEY")

print(LIARA_ENDPOINT)


s3=boto3.client("s3",endpoint_url=LIARA_ENDPOINT,aws_access_key_id=LIARA_ACCESS_KEY,aws_secret_access_key=LIARA_SECRET_KEY)

def upload_file(s3_client, bucket_name, file, file_name):
    try:
        s3_client.upload_fileobj(file, bucket_name, file_name)
        st.success(f"File '{file_name}' uploaded successfully.")
    except Exception as e:
        st.error(f"Error uploading file: {e}")



with open (file="book_test.pdf",mode="rb") as file:
    upload_file(s3,bucket_name=LIARA_BUCKET_NAME,file=file,file_name="book_test.pdf")