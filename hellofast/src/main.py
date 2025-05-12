from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated


class Item(BaseModel):
    name: str
    desc: str
    price: float
    tax: float | None = None


class QBody(BaseModel):
    q: Annotated[str | None, Field(default=None, max_length=3)]


app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/items/")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.put("/items/")
async def update_item(q: QBody):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q.q:
        results.update({"q": q.q})
    return results
