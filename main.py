from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create-posts")
async def create_post(newpost: Post):
    print(newpost)
    print(newpost.dict())
    return {"data": "newpost"}


@app.post("/create-posts2")
async def create_post2(payload: dict = Body(...)):
    print(payload)
    return {"data": "newpost"}
