from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from app.middleware.request_logger import RequestLoggerMiddleware
from app.handlers import honeypot_handlers
from app.routes import directory  # uniquement le routeur directory
from app.directory_cache import print_directory_history
from app.directory_files import directory_files  # pour le cache des fichiers
from app.prompt_fake_files import fake_files  # Assurez-vous que ce chemin est correct
from app.directory_cache import add_to_directory_history
from .config import text_file_extensions
import json
import os

serv = FastAPI()

# Mount static files (pour favicon notamment)
serv.mount("/static", StaticFiles(directory="static"), name="static")

# Include only directory router
serv.include_router(directory.router)

# Add logging middleware
serv.add_middleware(RequestLoggerMiddleware)

@serv.on_event("startup")
async def initialize_directory_cache():
    add_to_directory_history("/directory/", fake_files)


@serv.get("/")
async def root_redirect():
    return RedirectResponse(url="/directory/")


@serv.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    method = request.method
    path = request.url.path
    requete = (
        f"path = \"{path}\"\n"
    )
    ext = os.path.splitext(path)[1].lower()
    if method == "GET":
        # 1. In the case of a directory
        if path.endswith('/'):
            return await honeypot_handlers.handle_fake_directory(request, requete)
        # 2. In the case of a file
        elif ext in text_file_extensions:
            if ext == ".html":
                return await honeypot_handlers.handle_html(request, requete)
            elif ext == ".txt":
                return await honeypot_handlers.handle_txt(request, requete)
            elif ext == ".js":
                return await honeypot_handlers.handle_js(request, requete)
            elif ext == ".py":
                return await honeypot_handlers.handle_py(request, requete)
            else:
                return await honeypot_handlers.handle_other_extensions(request, requete)
        else:
            return RedirectResponse(url="/directory/")
    elif method == "POST":
            return await honeypot_handlers.handle_default_404(request)
            #return await honeypot_handlers.handle_post(request, requete)
    # 3. Else
    return await honeypot_handlers.handle_default_404(request)
    


@serv.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


#SamFul726386

#   

#uvicorn app.main:serv --reload
#cd D:\samyf\ecole\4A\stage\serveur\directory_serveur
#https://github.com/ollama/ollama/blob/main/docs/api.md


