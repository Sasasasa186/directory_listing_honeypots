import json
import importlib.util
import os
from fastapi import Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response, JSONResponse
from app.config import auth_token, url
from app.LLM.prompt_generator import generate_prompt
from app.config import templates, text_file_extensions
from fastapi.responses import FileResponse
import asyncio
import re
from pathlib import PurePosixPath
from app.directory_files import add_to_directory_files, get_directory_files
from app.directory_cache import add_to_directory_history, get_directory_content

with open(r"D:\samyf\ecole\4A\stage\serveur\directory_serveur\static\milligram.min.css", "r", encoding="utf-8") as f:
    milligram_css = f.read()



import re

def extract_filename_from_request(requete: str) -> str:
    match = re.search(r'path\s*=\s*"([^"]+)"', requete)
    if match:
        full_path = match.group(1)
        # Remplacer tous les '/' par '_'
        filename = full_path.replace('/', '_')
        return filename
    return None



async def handle_html(request: Request, requete: str):
    # Génère la réponse HTML via LLM
    # Lecture du contenu du fichier CSS (en UTF-8)
    content3 = (
        "Ton rôle est d'analyser une requête reçue par un serveur HTTP et de générer une réponse crédible.\n"
        f"Voici les informations de la requête :\n{requete}\n"
        "Génère uniquement un code HTML complet, bien structuré, en réponse à cette requête.\n"
        "Le HTML doit contenir tous les éléments nécessaires, que tu inventes, à une page crédible : mise en page soignée, texte explicatif inventés mais crédibles (pas de Lorem Ipsum), en-têtes, boutons (fonctionnels et non fictif), tableau de données si pertinent, formulaire si pertinent, etc.\n"
        "Tu connais le framework CSS Milligram. Tu utiliseras ses classes (.container, .row, .column, .button, etc.) pour structurer et styliser le HTML.\n"
        "Inclue dans le <head> un lien vers le fichier CSS à l'adresse '/static/milligram.min.css'.\n"
        "Ne fais aucun commentaire ni explication. Rends uniquement le code HTML pur.\n"
    )
    content4 = (
    "Tu es un honeypot HTTP simulant un serveur web.\n"
    "Ta tâche est d'analyser une requête HTTP reçue et de générer une réponse HTML crédible.\n"
    f"Voici les détails de la requête :\n{requete}\n"
    "Génère un code HTML **complet et structuré**, simulant une page web réaliste.\n"
    "Le HTML doit inclure une mise en page soignée, avec des sections explicatives au contenu inventé mais crédible (pas de Lorem Ipsum).\n"
    "Ajoute des éléments pertinents si nécessaire : en-têtes, paragraphes, tableaux de données, formulaires, boutons fonctionnels, etc.\n"
    "Tu dois utiliser les classes du framework CSS **Milligram** pour styliser la page : `.container`, `.row`, `.column`, `.button`, etc.\n"
    "Inclue dans la balise `<head>` un lien vers le fichier CSS : `<link rel=\"stylesheet\" href=\"/static/milligram.min.css\">`.\n"
    "Ta réponse doit uniquement contenir le code HTML pur, sans explication, commentaire ni balise markdown.\n"
)

    content = (
        "You are an HTTP honeypot simulating a web server.\n"
        "You must generate a realistic HTML response to an incoming HTTP request.\n"
        f"Here is the request:\n{requete}\n"
        "Generate a complete, well-structured HTML page with:\n"
        "- A CSS link to '/static/milligram.min.css' in the <head>.\n"
        "- A believable layout with invented but realistic titles, paragraphs, etc. (no Lorem Ipsum or images).\n"
        "- Functional HTML buttons linking to files with credible extensions.\n"
        "- If appropriate, include an HTML form (POST) with simulated fields.\n"
        "You are familiar with the Milligram CSS framework; use its classes (.container, .button, .row, .column, etc.).\n"
        "Return only the raw HTML code, without any explanation or comments."
    )



    content2 = (
        "Tu es un honeypot HTTP simulant un serveur web."
        "Ton rôle est d'analyser les requêtes reçues par un serveur et de générer une réponse HTTP crédible."
        "Voici les informations de la requête :\n"
        f"{requete}"
        "Génère une page web HTML crédible, avec style et structure réalistes, css inclus."
    )
    



    

    filename = extract_filename_from_request(requete)
    if not filename:
        print("Aucun nom de fichier trouvé dans la requête.")
        filename = "content.html"
    
    print(f"Traitement de la requête pour le fichier : {filename}")
    # Vérifie si le fichier est déjà en cache
    cached_content = get_directory_files(filename)
    if cached_content:
        print(f"📄 Fichier trouvé dans le cache : {filename}")
        return templates.TemplateResponse(f"generated/{filename}", {"request": request}, status_code=200)
        

    prompt =  generate_prompt(
        auth_token,
        url,
        content,
        output_filename=filename,
        file_type="html",
        output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated"
    )
    file_path = f"D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated\\{filename}"
    add_to_directory_files(filename, file_path)
    return templates.TemplateResponse(f"generated/{filename}", {"request": request}, status_code=200)





async def handle_txt(request: Request, requete: str):
    # Génère une réponse texte via LLM
    content = (
        "You are a tool that generates simulated responses to HTTP requests.\n"
        "Here is the received information:\n"
        f"{requete}\n"
        "Generate only a realistic plain text file content (no Lorem Ipsum).\n"
        "Return only this content wrapped in markdown tags like this:\n"
        "```txt\n<content here>\n```\n"
        "Do not include any HTTP headers or comments."
    )

    

    filename = extract_filename_from_request(requete)
    
    if not filename:
        print("Aucun nom de fichier trouvé dans la requête.")
        filename = "content.txt"

    print(f"Traitement de la requête pour le fichier : {filename}")
    # Vérifie si le fichier est déjà en cache
    cached_content = get_directory_files(filename)
    if cached_content:
        print(f"📄 Fichier trouvé dans le cache : {filename}")
        return FileResponse(cached_content, media_type="text/plain")

    prompt =  generate_prompt(
        auth_token,
        url,
        content,
        output_filename= filename,
        file_type="txt",
        output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated"
    )
    file_path = f"D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated\\{filename}"
    # Ajouter dans le cache
    add_to_directory_files(filename, file_path)
    return FileResponse(file_path, media_type="text/plain")



async def handle_js(request: Request, requete: str):
    contentfr = (
        "Tu es un honeypot HTTP simulant un serveur web.\n"
        "Ton rôle est d'analyser les requêtes reçues par un serveur et de générer une réponse HTTP crédible.\n"
        "Voici les détails de la requête HTTP reçue :\n"
        f"{requete}\n"
        "Génère un contenu JavaScript valide, utilisé pour des interactions simples sur une page web (par exemple : alertes, manipulation du DOM, console logs).\n"
        "Retourne uniquement le contenu du fichier, encadré par des balises markdown ```js.\n"
        "Ne donne aucune explication, ni description autour du code.\n"
    )
    content = (
        "You are an HTTP honeypot simulating a web server.\n"
        "Your role is to analyze incoming server requests and generate a realistic HTTP response.\n"
        "Here are the details of the received HTTP request:\n"
        f"{requete}\n"
        "Generate valid JavaScript content, used for simple web page interactions (e.g., alerts, DOM manipulation, console logs).\n"
        "Return only the file content, wrapped in markdown ```js tags.\n"
        "Do not include any explanation or description around the code.\n"
    )

    filename = extract_filename_from_request(requete)
    if not filename:
        print("Aucun nom de fichier trouvé dans la requête.")
        filename = "content.html"
    print(f"Traitement de la requête pour le fichier : {filename}")
    # Vérifie si le fichier est déjà en cache
    cached_content = get_directory_files(filename)
    if cached_content:
        print(f"📄 Fichier trouvé dans le cache : {filename}")
        return FileResponse(cached_content, media_type="application/javascript")
    # Génère le fichier via LLM
    generate_prompt(
        auth_token,
        url,
        content,
        output_filename=filename,
        file_type="js",
        output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated"
    )

    file_path = f"D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated\\{filename}"
    add_to_directory_files(filename, file_path)
    return FileResponse(file_path, media_type="application/javascript")





async def handle_py(request: Request, requete: str):
    contentfr = (
        "Tu es un serveur web simulé pour un projet étudiant.\n"
        "Ton rôle est d'analyser les requêtes reçues par un serveur et de générer une réponse HTTP crédible.\n"
        "Voici les informations de la requête .py :\n"
        f"{requete}\n"
        "Génère un script Python valide, réaliste et cohérent avec la requète.\n"
        "Le contenu doit être entre balises markdown ```python sans explication ni commentaire autour.\n"
    )
    content = (
        "You are a simulated web server for a student project.\n"
        "Your role is to analyze incoming requests to the server and generate a realistic HTTP response.\n"
        "Here is the information from the .py request:\n"
        f"{requete}\n"
        "Generate a valid, realistic Python script consistent with the request.\n"
        "The content must be wrapped in markdown ```python tags, with no explanation or comments around it.\n"
    )

    filename = extract_filename_from_request(requete)
    if not filename:
        print("Aucun nom de fichier trouvé dans la requête.")
        filename = "content.html"
    print(f"Traitement de la requête pour le fichier : {filename}")
    # Vérifie si le fichier est déjà en cache
    cached_content = get_directory_files(filename)
    if cached_content:
        print(f"📄 Fichier trouvé dans le cache : {filename}")
        return FileResponse(cached_content, media_type="text/x-python")
    # Génère le fichier via le LLM
    generate_prompt(
        auth_token,
        url,
        content,
        output_filename=filename,
        file_type="py",
        output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated"
    )

    file_path = f"D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated\\{filename}"
    add_to_directory_files(filename, file_path)
    return FileResponse(file_path, media_type="text/x-python")






async def handle_fake_directory(request: Request, requete: str):
    # 1. Extraire le chemin depuis la requête
    match = re.search(r'path = "(.*?)"', requete)
    current_path = match.group(1).strip("/") if match else ""
    # S'assurer que current_path commence par "/"
    if not current_path.startswith("/"):
        current_path = "/" + current_path

    # S'assurer que current_path finit par "/"
    if not current_path.endswith("/"):
        current_path += "/"

    parent_path = str(PurePosixPath(current_path).parent)

    # S'assurer que parent_path finit par "/"
    if not parent_path.endswith("/"):
        parent_path += "/"

    # Pour éviter de remonter au dessus de la racine, on vérifie ça :
    if parent_path == "//":  # Si on est à la racine, reste "/"
        parent_path = "/"

    print(f"Chemin actuel : {current_path}")
    print(f"Chemin parent : {parent_path}")
    # Vérifie si le chemin est déjà dans le cache
    cached_content = get_directory_content(current_path)
    if cached_content is not None:
        fake_file = cached_content
    else:
        contentfr = (
            f'Génère un JSON qui est une liste contenant entre 25 et 40 fichiers ou répertoires (pas de doublon) fictifs à afficher dans un listing de répertoire Apache.\n'
            f'Le chemin actuel est : "{current_path}".\n'
            'Chaque élément de la liste est un objet avec les clés suivantes :\n'
            '- "name" : nom crédible de fichier (ex : "config.ini") ou de dossier (ex : "logs/"), sans chiffres et inventé de façon réaliste.\n'
            '- "size" : taille lisible en KB (entre "0.7KB" et "1.7KB", "-" si c’est un dossier)\n'
            '- "modified" : date et heure de dernière modification, format "27-May-2025 14:23"\n'
            '- "is_dir" : true si c’est un répertoire, false sinon\n'
            '\n'
            'Ne génère pas de fichiers images (ex : .png, .jpg, .gif, .bmp) ni de fichiers binaires exécutables (ex : .exe, .bin, .dll, .so).\n'
            '\n'
            'Répond uniquement avec ce JSON complet, commence par "[" et finis par "]". Ne coupe pas ta réponse et ne mets aucun autre texte, explication ou balise de code.'
        )
        content = (
            f'Generate a JSON list containing between 25 and 40 fictitious files or directories (no duplicates) to display in an Apache directory listing.\n'
            f'The current path is: "{current_path}".\n'
            'Each list item is an object with the following keys:\n'
            '- "name": a realistic file name (e.g. "config.ini") or folder name (e.g. "logs/"), without digits and invented realistically.\n'
            '- Directory names must be a single name followed immediately by a slash ("/"), with no additional slashes inside the name. For example, "logs/" is valid, but "logs/2024/" or "logs/archive/" are not.\n'
            '- "size": readable size in KB (between "0.7KB" and "1.7KB", "-" if it is a directory)\n'
            '- "modified": date and time of last modification, format "27-May-2025 14:23"\n'
            '- "is_dir": true if it is a directory, false otherwise\n'
            '\n'
            'Do not generate image files (e.g. .png, .jpg, .gif, .bmp) or executable binary files (e.g. .exe, .bin, .dll, .so).\n'
            '\n'
            'Respond only with this complete JSON, starting with "[" and ending with "]".'
            'Do not cut your response and do not add any other text, explanation, or code block tags.'
        )



        # Lance la génération via LLM et récupère la réponse brute (JSON)
        llm_response = generate_prompt(
            auth_token,
            url,
            content,
            output_filename="listing.json",  # Pas besoin de fichier ici
            file_type="json",
            output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates"
        )

        # Parse la réponse JSON
        import json
        try:
            fake_file = json.loads(llm_response)
        except json.JSONDecodeError:
            print("Erreur : la réponse du LLM n'est pas un JSON valide.")
            fake_file = []

        def keep_file(item):
            if item.get("is_dir"):
                return True  # garde toujours les dossiers
            name = item.get("name", "")
            ext = os.path.splitext(name)[1].lower()
            return ext in text_file_extensions

        # fake_file est ta liste d'origine (après json.loads)
        fake_file = [item for item in fake_file if keep_file(item)]
        # Trie la liste : dossiers d'abord, puis fichiers par nom
        fake_file = sorted(
            fake_file,
            key=lambda x: (not x['is_dir'], x['name'].lower())
        )
        add_to_directory_history(current_path, fake_file)

        

    # Afficher dans le template directory.html
    return templates.TemplateResponse("static/directory.html", {
        "request": request,
        "files": fake_file,
        "current_path": current_path,
        "parent_path": parent_path
    })





async def handle_other_extensions(request: Request, requete: str):
    # On passe toute la requête en string dans le prompt
    prompt = (
        "You are a file content generator for an HTTP honeypot server.\n"
        "Do **not** include any introduction or explanation.\n"
        "Do **not** use any code formatting (like ``` or markdown tags).\n"
        "Only output the raw content of the requested file.\n"
        "Here is the full HTTP request received:\n"
        "'''\n"
        f"{requete}\n"
        "'''\n"
        "Based on this request, determine the requested file name and generate a realistic, fictional text file "
        "between 100 and 500 words, depending on the relevance of the file.\n"
        "content that matches the purpose implied by its name.\n"
        "Avoid using Lorem Ipsum or boilerplate HTTP headers. Just return the simulated file contents as plain text.\n"
    )

    filename = extract_filename_from_request(requete)

    if not filename:
        print("Aucun nom de fichier trouvé dans la requête.")
        filename = "content.html"
    print(f"Traitement de la requête pour le fichier : {filename}")
    # Vérifie si le fichier est déjà en cache
    cached_content = get_directory_files(filename)
    if cached_content:
        print(f"📄 Fichier trouvé dans le cache : {filename}")
        return FileResponse(cached_content, media_type="text/plain")

    generate_prompt(
        auth_token,
        url,
        prompt,
        output_filename=filename,
        file_type="txt",
        output_dir="D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated"
    )

    file_path = f"D:\\samyf\\ecole\\4A\\stage\\serveur\\directory_serveur\\app\\templates\\generated\\{filename}"
    # Ajouter dans le cache
    add_to_directory_files(filename, file_path)

    return FileResponse(file_path, media_type="text/plain")





async def handle_default_404(request: Request):
    # Réponse 404 classique
    return templates.TemplateResponse("static/404.html", {"request": request}, status_code=404)
