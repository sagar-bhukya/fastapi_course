from pydantic import BaseModel
from fastapi import FastAPI
from  typing import List,Dict

app=FastAPI()
fake_db:Dict[int,dict]={}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int

items_db = []

@app.post('/items/')
async def post_fun(item:Item):
    items_db.append(item)
    return item
