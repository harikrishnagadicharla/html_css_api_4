# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory "database"
items = []

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add")
def create_item(id: int = Form(...), name: str = Form(...), description: str = Form(""), price: float = Form(...)):
    for item in items:
        if item["id"] == id:
            return RedirectResponse("/", status_code=303)
    items.append({"id": id, "name": name, "description": description, "price": price})
    return RedirectResponse("/", status_code=303)

@app.get("/delete/{item_id}")
def delete_item(item_id: int):
    global items
    items = [item for item in items if item["id"] != item_id]
    return RedirectResponse("/", status_code=303)
