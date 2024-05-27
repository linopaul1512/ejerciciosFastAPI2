from fastapi  import FastAPI, Form, HTTPException
from typing import Annotated


app= FastAPI()

items = {"foo": "The foo wrestler"}


@app.get("/items/{item_id}")
async def read_item(item_id: str): 
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Ite, not found")
    return {"item": items[item_id]}
