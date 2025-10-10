import json
import os
import asyncio
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from app.config import templates
from starlette.websockets import WebSocketDisconnect


router = APIRouter()

BASE_LOG_PATH = "D:/samyf/ecole/4A/stage/serveur/directory_serveur"

# Fonction pour lire tout le contenu du fichier au début
async def read_all_lines(file_path):
    lines = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    lines.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        pass
    return lines

# Fonction pour suivre les nouvelles lignes à partir d'un offset
async def follow_file(file_path, offset):
    new_lines = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.seek(offset)
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    new_lines.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
            new_offset = f.tell()
            return new_lines, new_offset
    except FileNotFoundError:
        return [], offset

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Initialisation des offsets pour cette connexion
    offsets = {
        "requests_log.jsonl": 0,
        "directory_history.jsonl": 0,
        "directory_files.jsonl": 0,
    }

    try:
        # Lecture et envoi initial
        initial_data = {}
        for file_name in offsets.keys():
            file_path = os.path.join(BASE_LOG_PATH, file_name)
            lines = await read_all_lines(file_path)
            if lines:
                key = file_name.replace(".jsonl", "")
                initial_data[key] = lines

                # Mettre à jour l'offset pour chaque fichier
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        f.seek(0, os.SEEK_END)
                        offsets[file_name] = f.tell()
                except FileNotFoundError:
                    pass

        if initial_data:
            await websocket.send_text(json.dumps(initial_data))

        # Boucle d’envoi des nouvelles lignes
        while True:
            data_to_send = {}

            for file_name in offsets.keys():
                file_path = os.path.join(BASE_LOG_PATH, file_name)
                new_lines, new_offset = await follow_file(file_path, offsets[file_name])
                if new_lines:
                    key = "new_" + file_name.replace(".jsonl", "")
                    data_to_send[key] = new_lines
                    offsets[file_name] = new_offset

            if data_to_send:
                await websocket.send_text(json.dumps(data_to_send))

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client déconnecté proprement")
    except Exception as e:
        print(f"Erreur WebSocket : {e}")
