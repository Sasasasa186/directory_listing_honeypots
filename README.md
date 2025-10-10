# HTTP Honeypot Directory Listing Simulator

Un honeypot HTTP simulant un service de **directory listing**, générant dynamiquement des fichiers et dossiers fictifs grâce à un **modèle LLM**. Idéal pour des **tests pédagogiques, démonstrations ou études de sécurité**.

---

## 🔹 Fonctionnalités

* Simule un serveur Apache avec listing de répertoires.
* Génère le nom/taille/date des fichiers HTML, TXT, JS, PY et autres extensions textuelles ainsi que sous_dossier de manière réaliste.
* Génère le contenu des fichiers HTML, TXT, JS, PY et autres extensions textuelles de manière réaliste.
* Classe les fichiers et dossiers comme dans un vrai listing (`Parent Directory`, dossiers d’abord, fichiers ensuite).
* Middleware de logging pour enregistrer toutes les requêtes dans un fichier JSONL.
* Caches en mémoire et sur disque pour accélérer les réponses et limiter les appels au LLM.
* Utilise **FastAPI** pour un serveur léger et rapide.

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
API_URL=http://127.0.0.1:11434/api/generate
AUTH_TOKEN=ta_clef_api_ici
```

> ⚠️ **Ne jamais versionner `.env`**. Il contient des informations sensibles.

---

## 📂 Structure des dossiers

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
logs/
 └─ requests_log.jsonl  # toutes les requêtes entrantes
```

* `logs/` et `generated/` sont **exclus de GitHub** via `.gitignore`.

---

## 🚀 Lancement

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

## 📄 Licence

* Projet : **MIT License**
* Milligram CSS : **MIT License** ([milligram.io](https://milligram.io/))

---
