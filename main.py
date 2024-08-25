from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
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


my_posts = [{"title": "hello1", "content": "world1", "id": 1}, {"title": "hello2", "content": "world2", "id": 2}]


@app.get("/create-posts3")
async def create_post3():
    return {"data": my_posts}


@app.post("/create-posts4")
async def create_post4(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": my_posts}


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/posts/{id}")
async def get_posts(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    my_posts.pop(index)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post sssss id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    post_dict["title"] = post.title
    post_dict["content"] = post.content
    post_dict["published"] = post.published
    my_posts[index] = post_dict
    return {"data": post_dict}
