from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config import templates
import re
from app.prompt_fake_files import fake_files  # Assurez-vous que ce chemin est correct
from app.directory_cache import add_to_directory_history
router = APIRouter()




@router.get("/directory/", response_class=HTMLResponse)
async def fake_directory_listing(request: Request):

    return templates.TemplateResponse(f"static/directory.html", {
        "request": request,
        "current_path": "/directory/",
        "files": fake_files
    })
