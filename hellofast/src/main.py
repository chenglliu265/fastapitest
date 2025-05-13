from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Annotated


class Item(BaseModel):
    name: str
    desc: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
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


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


class QItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: QItem, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.delete("/items/{item_id}")
async def del_item(item_id: int):
    result = [
        {"item_id": 1, "name": "Python", "desc": "", "price": 12.88, "tax": 1.35},
        {"item_id": 2, "name": "Java", "desc": "", "price": 12.98, "tax": 1.27},
    ]
    result = [item for item in result if item["item_id"] != item_id]
    return result
