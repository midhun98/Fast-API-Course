from random import randrange
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


@app.post("/posts")
async def create_post(newpost: Post):
    print(newpost)
    print(newpost.dict())
    return {"data": "newpost"}


@app.post("/create-posts2")
async def create_post2(payload: dict = Body(...)):
    print(payload)
    return {"data": "newpost"}

my_posts = [{"title": "hello1", "content": "world1"}, {"title": "hello2", "content": "world2"}]

@app.get("/create-posts3")
async def create_post3():
    return {"data": my_posts}

@app.post("/create-posts4")
async def create_post3(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": my_posts}