from models.notes import Note
from config.db import conn
from schemas.notes import noteEntity, notesEntity
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.notes import noteEntity,notesEntity
from bson import ObjectId 


note = APIRouter()

templates = Jinja2Templates(directory="templates")

# @note.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     newDoc = []
#     docs = conn.Notes.Notes.find({})
#     for doc in docs:
#         newDoc.append({
#             "id": doc['_id'],
#             'title': doc['title'],
#             'desc': doc['desc'],
#             'important' : doc['important']
#         })
#     return templates.TemplateResponse(
#         request=request, name="index.html",  context={"Docs": newDoc}
#     )


@note.get("/")
async def read_item(request: Request,  title: str = None):
    
    query_filter = {}
    if title:
        query_filter['title'] = title

    docs = conn.Notes.Notes.find(query_filter)
    # newDoc = notesEntity(docs)  # this is for multiple data

    # this is for by single data
    newDoc = []
    for doc in docs:
        newDoc.append(
            noteEntity(doc)
        )

    return {'Docs' : newDoc}
        


# @note.post("/")
# async def create_item(request: Request):
#     form = await request.form()
#     print(form)

#     formDict = dict(form)

#     # Validation: Check if required fields are present
#     # required_fields = ["title", "desc"]
#     # missing_fields = [field for field in required_fields if not formDict.get(field)]

#     # if missing_fields:
#     #     raise HTTPException(
#     #         status_code=422,
#     #         detail={
#     #             "error": "Missing required fields.",
#     #             "missing_fields": missing_fields,
#     #         },
#     #     )

#     formDict['important'] = False if formDict['important'] == 'false' else True

#     note = conn.Notes.Notes.insert_one(formDict)
   
#     return {'Success' : True}



@note.put("/")
async def update_note(id:str, title:str = None, desc:str = None, important:bool = None):
    update_data = {}
    if title:
        update_data['title'] = title
    if desc:
        update_data['desc'] = desc
    if important is not None:
        update_data['important'] = important

    # Check if there's any update data
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Convert the string id to ObjectId, which MongoDB uses as the identifier
    object_id = ObjectId(id)

    # Perform the update operation
    result = conn.Notes.Notes.update_one({'_id': object_id}, {'$set': update_data})

    # Check if the document was found and updated
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    # Return the updated document (if desired, or a success message)
    updated_note = conn.Notes.Notes.find_one({'_id': object_id})
    return {'message': 'Note updated successfully', 'note': noteEntity(updated_note)}





@note.post("/")
async def create_note(note_request: Note):
    # Build the document to insert
    new_note = {
        "title": note_request.title,
        "desc": note_request.desc,
        "important": note_request.important
    }

    # Insert the new note into MongoDB
    result = conn.Notes.Notes.insert_one(new_note)
    
    # Check if the insertion was successful
    if result.inserted_id:
        # Convert ObjectId to string
        new_note['id'] = result.inserted_id
        
        return {"message": "Note created successfully", "note": noteEntity(new_note)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create note")