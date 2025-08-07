from fastapi import FastAPI
from models.models import Base
from router import user_router,book_router

from db import engine

Base.metadata.create_all(bind = engine)

app=FastAPI(title = "library API")

Base.metadata.create_all(bind=engine)
app.include_router(router = user_router.router,tags =  ["auth"])
app.include_router(router = user_router.user_router,tags = ["user"])
app.include_router(router = book_router.file_router,tags = ["book"])

@app.get("/")
def welcome() -> str:
    
    return "welcome friends :0"

