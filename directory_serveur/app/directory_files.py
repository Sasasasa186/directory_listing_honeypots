# directory_cache.py
import json, os
from collections import OrderedDict

# Nombre maximum d'éléments dans l'historique
MAX_HISTORY = 100
FILES_JSONL_PATH = "D:/samyf/ecole/4A/stage/serveur/directory_serveur/directory_files.jsonl"
DIRECTORY_SERVEUR_ROOT = r"D:\samyf\ecole\4A\stage\serveur\directory_serveur\app\templates\generated"

# Dictionnaire pour stocker les chemins et contenus
directory_files = OrderedDict()  # clé = chemin, valeur = contenu (liste de fichiers/dossiers)


def add_to_directory_files(path: str, content: list):
    global directory_files

    if path in directory_files:
        print(f"🔁 Clé déjà présente dans le cache : {path} → contenu non modifié.")
        return

    # Si le cache est plein, supprimer le plus ancien
    if len(directory_files) >= MAX_HISTORY:
        directory_files.popitem(last=False)

    # Ajouter la nouvelle entrée
    directory_files[path] = content
    print(f"✅ Ajout au cache : {path} ({len(content)} élément{'s' if len(content) > 1 else ''})")
    normalized_path = path.replace("_", "/")
    save_file_entry_to_jsonl(normalized_path, content)

def save_file_entry_to_jsonl(path: str, content: list):

    try:
        with open(content, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        file_content = f"[Erreur] Fichier non trouvé : {path}"
    except Exception as e:
        file_content = f"[Erreur de lecture] {str(e)}"

    line = {
        "path": path,
        "entries": file_content
    }

    with open(FILES_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")





def get_directory_files(path: str):
    """Retourne le contenu stocké pour un chemin, ou None s'il n'est pas en cache."""
    return directory_files.get(path)


# Ajoute ceci à la fin du fichier :
def print_directory_files():
    print("\n--- Contenu du cache des fichiers ---")
    for path, content in directory_files.items():
        print(f"📁 {path} ({len(content)} éléments)")
        for entry in content:
            print(f"   └─ {entry['name']} ({'Dossier' if entry['is_dir'] else 'Fichier'})")
    print("------------------------------------------\n")

def clear_history():
    """Réinitialise tout l'historique."""
    directory_files.clear()
