from models.notes import Note
from config.db import conn
from schemas.notes import noteEntity, notesEntity
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


note = APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
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


@note.post("/")
def add_note(note1: Note):
    print(note1)
    inserted_note = conn.notes.notes.insert_one(dict(note1))
    return noteEntity(inserted_note)