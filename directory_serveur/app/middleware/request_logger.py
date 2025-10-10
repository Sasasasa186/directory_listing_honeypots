# app/middleware/logger.py
import json
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.config import LOG_FILE_PATH

logging.basicConfig(level=logging.INFO)

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Lire le corps de la requête sans le consommer définitivement
        body_bytes = await request.body()
        try:
            body_json = json.loads(body_bytes.decode())
        except:
            body_json = body_bytes.decode(errors="ignore")

        # Recréer la requête avec un flux non consommé
        async def receive() -> dict:
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request = Request(request.scope, receive)

        # Infos utiles
        client_ip = request.client.host if request.client else "unknown"
        x_usage = request.headers.get("x-usage", None)

        request_info = {
            "method": request.method,
            "path": request.url.path,
            "url": str(request.url),
            "client_ip": client_ip,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "cookies": dict(request.cookies),
            "body": body_json,
        }

        if x_usage:
            request_info["x_usage"] = x_usage

        logging.info("Requête interceptée : %s", json.dumps({"url": str(request.url)}))

        # Mesure de performance
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000

        # Ne lis surtout pas response.body ici (sauf si tu le traites correctement)
        response_info = {
            "status_code": response.status_code,
            "process_time_ms": round(duration_ms, 2),
            "headers": dict(response.headers),
        }

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            json.dump({"request": request_info, "response": response_info}, f, ensure_ascii=False)
            f.write("\n")

        return response
