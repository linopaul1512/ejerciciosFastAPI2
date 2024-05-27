from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Any

from fastapi import FastAPI
app = FastAPI()
@app.get('/item/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}

