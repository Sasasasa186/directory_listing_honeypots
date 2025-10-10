# directory_cache.py
import json
from collections import OrderedDict

# Nombre maximum d'éléments dans l'historique
MAX_HISTORY = 15

# Dictionnaire pour stocker les chemins et contenus
directory_history = OrderedDict()  # clé = chemin, valeur = contenu (liste de fichiers/dossiers)
HISTORY_FILE_PATH = "D:/samyf/ecole/4A/stage/serveur/directory_serveur/directory_history.jsonl"


def add_to_directory_history(path: str, content: list):
    global directory_history

    # Si déjà présent, on le supprime pour le remettre à la fin
    if path in directory_history:
        del directory_history[path]
    elif len(directory_history) >= MAX_HISTORY:
        # Supprimer l'entrée la plus ancienne
        directory_history.popitem(last=False)

    # Ajouter la nouvelle entrée
    directory_history[path] = content
    save_entry_to_jsonl(path, content)


def get_directory_content(path: str):
    """Retourne le contenu stocké pour un chemin, ou None s'il n'est pas en cache."""
    return directory_history.get(path)


# Ajoute ceci à la fin du fichier :
def print_directory_history():
    print("\n--- Contenu du cache des répertoires ---")
    for path, content in directory_history.items():
        print(f"📁 {path} ({len(content)} éléments)")
        for entry in content:
            print(f"   └─ {entry['name']} ({'Dossier' if entry['is_dir'] else 'Fichier'})")
    print("------------------------------------------\n")

def save_entry_to_jsonl(path: str, content: list):
    """Ajoute une ligne dans le fichier JSONL pour chaque nouvelle entrée."""
    line = {
        "path": path,
        "entries": content
    }

    with open(HISTORY_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def clear_history():
    """Réinitialise tout l'historique."""
    directory_history.clear()
