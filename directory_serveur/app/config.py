# app/config.py
import os
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

auth_token = os.getenv("AUTH_TOKEN")
url = os.getenv("SERVER_URL")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "requests_log.jsonl")

# Crée une instance de Jinja2Templates avec le répertoire des templates
templates = Jinja2Templates(directory="app/templates")


text_file_extensions = [
    ".txt", ".md", ".rtf", ".html", ".css", ".js", ".py", ".php", ".java", ".cpp", ".c",
    ".cs", ".sh", ".bat", ".sql", ".json", ".xml", ".yaml", ".yml", ".ini", ".cfg",
    ".conf", ".log", ".tex", ".csv", ".toml", ".env", ".properties", ".asm", ".go",
    ".rb", ".pl", ".vb", ".r", ".swift", ".kt", ".scss", ".less", ".vue", ".ts", ".tsx",
    ".jsx", ".gradle", ".gradle.kts", "Dockerfile", "Makefile", ".adoc", ".nfo", ".cmake",
    ".podspec", ".proto", ".gitignore", ".gitattributes", ".podspec", ".ld", ".d"
]
