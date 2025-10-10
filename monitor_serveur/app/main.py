
from fastapi import FastAPI
from app.routes import directory  # importe le router depuis directory.py
from fastapi.staticfiles import StaticFiles

serv = FastAPI()

# Inclure le router directory à l'application principale
serv.include_router(directory.router)  # prefix vide, les routes sont "/", "/api/paths", etc.

#uvicorn app.main:serv --reload --port 8001
#cd D:\samyf\ecole\4A\stage\serveur\monitor_serveur
#https://github.com/ollama/ollama/blob/main/docs/api.md


