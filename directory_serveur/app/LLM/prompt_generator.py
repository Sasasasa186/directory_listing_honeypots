from app.config import auth_token, url
import requests
import json
import re
import os


def process_streamed_response(response, file_type= None,  output_filename="erreur.html", output_dir="."):
    full_response = ""
    # Lire chaque ligne de la réponse streamée
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                full_response += data["message"]["content"]

    content_to_save = full_response

    if file_type == "html":
        # Extraction du bloc HTML (doctype + balises html)
        match = re.search(r"(<!DOCTYPE html.*?>.*?</html>)", full_response, re.DOTALL | re.IGNORECASE)
        if match:
            print("Bloc HTML trouvé, extraction en cours...")
            content_to_save = match.group(1).strip()
        else:
            print("Aucun code HTML trouvé dans la réponse, sauvegarde tout le contenu brut.")

    elif file_type == "py":
        debut = full_response.find("```python")
        if debut != -1:
            print("Bloc de code Python trouvé, extraction en cours...")
            content_to_save = full_response[debut + len("```python"):].strip()
            # Optionnel : retirer une éventuelle fin de bloc s'il y en a une
            fin = content_to_save.find("```")
            if fin != -1:
                content_to_save = content_to_save[:fin].strip()
        else:
            print("Aucun bloc de code Python trouvé dans la réponse, sauvegarde tout le contenu brut.")
    
    elif file_type == "txt":
        debut = full_response.find("```txt")
        if debut != -1:
            print("Bloc de code texte trouvé, extraction en cours...")
            content_to_save = full_response[debut + len("```txt"):].strip()
            # Optionnel : retirer une éventuelle fin de bloc s'il y en a une
            fin = content_to_save.find("```")
            if fin != -1:
                content_to_save = content_to_save[:fin].strip()
        else:
            print("Aucun bloc de code texte trouvé dans la réponse, sauvegarde tout le contenu brut.")

    elif file_type == "js":
        # Cherche d'abord ```javascript
        debut = full_response.find("```javascript")
        if debut == -1:
            # Si pas trouvé, cherche ```js
            debut = full_response.find("```js")
        if debut != -1:
            print("Bloc de code JavaScript trouvé, extraction en cours...")
            content_to_save = full_response[debut:].split('\n', 1)[1]  # enlève la ligne ```js ou ```javascript
            fin = content_to_save.find("```")
            if fin != -1:
                content_to_save = content_to_save[:fin].strip()
        else:
            print("Aucun bloc de code JavaScript trouvé dans la réponse, sauvegarde tout le contenu brut.")
            content_to_save = full_response.strip()

    elif file_type == "json":
        # Cherche un bloc ```json ... ```
        debut = full_response.find("```json")
        if debut != -1:
            print("Bloc JSON trouvé, extraction en cours...")
            content_to_save = full_response[debut + len("```json"):].strip()
            # Retirer une éventuelle fin de bloc ```
            fin = content_to_save.find("```")
            if fin != -1:
                content_to_save = content_to_save[:fin].strip()
        else:
            # Pas de bloc JSON délimité, on suppose que la réponse est brute JSON
            print("Aucun bloc JSON délimité trouvé, tentative de sauvegarde brute.")
            content_to_save = full_response.strip()
    else:
        print(f"Type de fichier '{file_type}' non pris en charge pour extraction spécifique.")
        # On sauvegarde quand même tout le contenu

    # Création du répertoire si nécessaire
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, output_filename)

    # Écriture dans le fichier
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content_to_save)

    print(f"Le fichier {output_filename} a été enregistré sous '{output_path}'.")
    return content_to_save


def generate_prompt(
    auth_token=auth_token,
    url=url,
    prompt=None,
    model="llama3.1:8b",
    file_type= None,
    output_filename="erreur.html",
    output_dir="app"
):
    if prompt is None:
        print("No prompt provided. Using default prompt.")

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "options": {
            "seed": 101,
            "temperature": 0
        },
        "stream": True
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, stream=True)
    except requests.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")
        return None
    
    if response.status_code == 200:
        return process_streamed_response(
            response,
            file_type=file_type,
            output_filename=output_filename,
            output_dir=output_dir,
        )
    else:
        print(f"Error during request: {response.status_code}")
        print(response.text)
        return None
