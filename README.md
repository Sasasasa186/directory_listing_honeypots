# HTTP Honeypot Directory Listing Simulator

Un honeypot HTTP simulant un service de **directory listing**, générant dynamiquement des fichiers et dossiers fictifs grâce à un **modèle LLM**. Idéal pour des **tests pédagogiques, démonstrations ou études de sécurité**.

## Structure du projet

Le projet contient deux serveurs FastAPI :

1. **Directory Server (`directory_serveur/`)**
   - Honeypot HTTP simulant un service de directory listing.
   - Fichiers principaux :
     - `requests_log.jsonl` (requétes recuts par le serveur)
     - `directory_history.jsonl` (historique des répertoires générés par le LLM)
     - `directory_files.jsonl` (contenu des fichiers générés par le LLM)
   - Les fichiers `.jsonl` doivent être placés directement dans `directory_serveur/`.

2. **Monitoring Server (`monitor_serveur/`)**
   - Affiche en temps réel l’historique du Directory Server (requétes et fichiers/dossiers générés).
   - Lit automatiquement tous les fichiers `.jsonl` présents dans `directory_serveur/` via WebSocket.

---

## 🔹 Fonctionnalités
### 🕵️‍♂️ Honeypot HTTP
* Simule un serveur HTTP de type listing de répertoires.
* Génère le nom/taille/date des fichiers HTML, TXT, JS, PY et autres extensions textuelles ainsi que des sous_dossier de manière réaliste.
* Génère le contenu des fichiers HTML, TXT, JS, PY et autres extensions textuelles de manière réaliste.
* Middleware pour enregistrer toutes les requêtes dans un fichier JSONL.
* Utilise **FastAPI** pour un serveur léger et rapide.

### 📡 Monitoring en temps réel
* Serveur FastAPI avec WebSocket.
* Affiche en direct :
  - Les requêtes HTTP reçues.
  - L’historique des répertoires.
  - Les fichiers exposés.
---

## 🛠️ Installation

1. **Cloner le dépôt**

2. **Créer un environnement Python**

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Créer le fichier `.env`**

Crée un fichier `.env` à la racine avec les variables suivantes :

```env
API_URL=adresse url de l'api pour le LLM
AUTH_TOKEN=ta_clef_api_ici
```

> ⚠️ **Ne jamais versionner `.env`**. Il contient des informations sensibles.

---

## 📂 Structure des dossiers pour directory_serveur

```
app/
 ├─ templates/
 │   ├─ static/
 │   │   ├─ directory.html
 │   │   └─ 404.html 
 │   └─ generated/      # fichiers générés par le LLM (non versionnés)
 ├─ routes/             # routeur pour le listing
 ├─ handlers/           # gestion des requêtes par type de fichier
 ├─ middleware/         # logger HTTP
 ├─ config.py           # configuration globale
 ├─ directory_cache.py  # cache des dossiers
 ├─ directory_files.py  # cache des fichiers
 └─ prompt_fake_files.py
 
static/
 ├─ milligram.min.css
 └─ favicon.ico
├─ requests_log.jsonl  # toutes les requêtes entrantes
├─ directory_history.jsonl #tous les dossiers générés
└─ directory_files.jsonl #tous les fichiers générés

```

* `logs/` et `generated/` sont **exclus de GitHub** via `.gitignore`.

---

## 🚀 Lancement des serveurs

```bash
uvicorn app.main:serv --reload
```

* Le serveur démarre sur `http://127.0.0.1:8000/`
* La racine `/` redirige vers `/directory/`

---

## 🔧 Utilisation

* Naviguer sur `/directory/` pour voir le listing simulé.
* Tous les fichiers générés sont **fictifs** et adaptés au nom de fichier demandé.
* Les extensions supportées incluent `.html`, `.txt`, `.js`, `.py` et autres extensions textuelles définies dans `config.py`.

---

## ⚙️ Configuration

* **Variables sensibles** : `.env` (`API_URL`, `AUTH_TOKEN`)
* **Cache mémoire et disque** :

  * `directory_cache.py` → cache des dossiers
  * `directory_files.py` → cache des fichiers
* **Logging** :

  * Middleware `RequestLoggerMiddleware` enregistre toutes les requêtes dans `logs/requests_log.jsonl`.

---

## 📚 Notes

* **Milligram CSS** : framework léger utilisé pour la mise en page (`static/milligram.min.css`), licence MIT.
* Les fichiers générés par le LLM ne doivent **jamais** contenir de données réelles.
* Ce projet est conçu pour **l’apprentissage et la simulation**, pas pour un serveur de production réel.

---

## 📝 Contributions

* Les contributions sont les bienvenues : correction de bugs, nouvelles extensions, amélioration des prompts.
* Merci de **ne pas inclure de clés API réelles** dans les PR.

---

## 🧑‍💻 Auteur
**Samy Fulchiron**  
[🔗 Profil LinkedIn](https://www.linkedin.com/in/samy-fulchiron-00538932b/)  
[🐙 GitHub](https://github.com/samy-fulchiron)

---

## 📄 Licence

* Projet : **MIT License**
* Milligram CSS : **MIT License** ([milligram.io](https://milligram.io/))

---
