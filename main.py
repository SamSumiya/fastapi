from typing import Optional
from fastapi import FastAPI, Request
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()


my_posts = [
    {"id": 1, "title": "Food", "content": "Best Pizza ever"}, 
    {"id": 2, "title": "Nature", "content": "Best lake is tahoe"}
]


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
    print(datetime.utcnow())
    return{"Data": my_posts}


@app.get('/posts/{id}')
def get_post(id: int):
    int_id = id - 1
    return{"Data": my_posts[int_id]}


"""
Title: Str
Content: Str
Date: Date UTC
"""
@app.post('/posts')
def create(payload: Post):
    dict = payload.dict()
    dict['id'] = random.randrange(1, 1000000)
    dict['date'] = datetime.utcnow() 
    my_posts.append(dict)
    return {"Message": dict}

