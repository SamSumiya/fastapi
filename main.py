from tarfile import HeaderError
from typing import Optional
from fastapi import FastAPI, Response, Request, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()


my_posts = [
    {"id": 1, "title": "Food", "content": "Best Pizza ever"}, 
    {"id": 2, "title": "Nature", "content": "Best lake is tahoe"}
]


def find_post(id): 
    for post in my_posts:
        if id == post['id']: 
            return id
    return False

def find_update_post(id: str): 
    for i, post in enumerate(my_posts):
        if id == post['id']: 
            return post
    return False


def update_post(id, payload) -> dict:  
    selected = my_posts[id - 1]
    selected['title'] = payload['title']
    selected['content'] = payload['content']
    return selected
    

class Post(BaseModel):
    id: int = random.randrange(1, 1000000000)
    title: str
    content: str = None
    published: bool = False
    rating: Optional[int] = None
    date: datetime = datetime.utcnow()




@app.get('/')
def root():
    return {'Message': "Hi People!"}


@app.get('/posts')
def get_posts():
    return{"Data": my_posts}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    iid = id - 1
    
    if iid > len(my_posts) - 1:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"data": "Not Found, try again with a different id else..."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Id {iid} was not found, try again with a different id else...")
    return {"data": my_posts[iid]}


"""
Title: Str
Content: Str
Date: Date UTC
"""
@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(payload: Post, response: Response):
    dict = payload.dict()
    dict['id'] = random.randrange(1, 1000000)
    dict['date'] = datetime.utcnow() 
    my_posts.append(dict)
    return {"Message": dict}


@app.put('/posts/{id}')
def put_post(id: int, payload: Post):
    post = find_update_post(id)
    print(post, 'waht is this post>')
    if post: 
        res = update_post(id, payload.dict())
        return {"posts": res}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doest not exit and can't update a none value")

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if post:
        my_posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT) 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist...")
