from typing import List

from uuid import uuid4

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

ITEMS = [
    {"id": str(uuid4()), "name": "item 1"},
    {"id": str(uuid4()), "name": "item 2"},
    {"id": str(uuid4()), "name": "item 3"},
]


class Item(BaseModel):
    class Name(BaseModel):
        name: str

    item: Name


class ResponseItem(BaseModel):
    id: str
    name: str


class ResponseListItem(BaseModel):
    items: List[ResponseItem]


class ResponseSingleItem(BaseModel):
    item: ResponseItem


@app.get("/")
def read_root():
    return {"Hello": "World"}


# item の CRUD の mock


@app.get("/items", response_model=ResponseListItem)
def read_items():
    return {"items": ITEMS}


@app.get("/items/{item_id}", response_model=ResponseSingleItem)
def read_item(item_id: str):
    for item in ITEMS:
        if item["id"] == item_id:
            return {"item": item}
    raise HTTPException(status_code=404, detail="Not Found")


@app.post("/items", status_code=201, response_model=ResponseSingleItem)
def create_item(item: Item):
    id_ = str(uuid4())
    new_item = {"id": id_, "name": item.item.name}
    ITEMS.append(new_item)
    return {"item": new_item}


@app.put("/items/{item_id}", response_model=ResponseSingleItem)
def update_item(item_id: str, req_item: Item):
    target_item = None
    for item in ITEMS:
        if item["id"] == item_id:
            target_item = item
    if not target_item:
        raise HTTPException(status_code=404, detail="Not Found")

    target_item["name"] = req_item.item.name
    return {"item": target_item}


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    item = None
    for i, item in enumerate(ITEMS):
        if item["id"] == item_id:
            del ITEMS[i]
    return
