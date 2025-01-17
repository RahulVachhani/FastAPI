# from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conn = MongoClient("mongodb+srv://Rahul:******@fastapi.k9cht.mongodb.net/")

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    newDoc = []
    docs = conn.Notes.Notes.find({})
    for doc in docs:
        newDoc.append({
            "id": doc['_id'],
            'note': doc['note']
        })
    return templates.TemplateResponse(
        request=request, name="index.html",  context={"Docs": newDoc}
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
