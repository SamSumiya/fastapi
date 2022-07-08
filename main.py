from typing import Optional
from fastapi import FastAPI, Response, Request
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()



my_posts = [
    {"id": 1, "title": "Food", "content": "Best Pizza ever"}, 
    {"id": 2, "title": "Nature", "content": "Best lake is tahoe"}
]


def update_post(id, payload) -> dict:  
    selected = my_posts[id - 1]
    print(payload, 'pdafdsafasdfsaf')
    print(selected, 'selected is here')
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
    print(datetime.utcnow())
    return{"Data": my_posts}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    iid = id - 1
    
    if iid > len(my_posts) - 1:
        response.status_code = 404
        return{"Data": "Not Found"}
    return {"Data": my_posts[iid]}


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


@app.put('/posts/{id}')
def create(id: int, payload: Post):
    res = update_post(id, payload.dict())
    return {"posts": res}