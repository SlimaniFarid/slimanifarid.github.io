# Blog Django — Farid Slimani

Blog dynamique (Django + SQLite) pour une mise en production sur **PythonAnywhere**.
Le dépôt, sur la branche `django_blog`, ne contient **que** le projet Django.

## Structure

```
slimanifarid.github.io/     # branche django_blog
  config/            # settings, urls, wsgi, asgi
  blog/              # app Django (Article, Category)
  templates/         # base.html, blog/article_list.html, blog/article_detail.html
  static/css/style.css
  manage.py
  requirements.txt   # Django==6.0.6
  pa_wsgi.py         # point d'entrée WSGI PythonAnywhere
```

## En local

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   # http://127.0.0.1:8000
```

- Admin : `python manage.py createsuperuser` puis `/admin/` — gérez catégories et articles (`Article` : titre, slug auto, catégorie, extrait, corps, publié, à la une).

---

## Déploiement sur PythonAnywhere

### 1. Cloner le dépôt dans la console bash de PythonAnywhere

```bash
git clone https://github.com/SlimaniFarid/slimanifarid.github.io.git
cd slimanifarid.github.io
git checkout django_blog
```

> Le dépôt est un *orphan* : sur la branche `django_blog` il ne contient que le projet Django (pas le portfolio statique). Pas de conflit de dossier `blog/`.

Dossier projet : `/home/VOTRE_USER/slimanifarid.github.io`

### 2. Créer le virtualenv et installer Django

```bash
mkvirtualenv djangoblog --python=/usr/bin/python3.12
pip install -r requirements.txt
```

> Vérifie la version Python dispo : `ls /usr/bin/python3*`. Adapter `--python` si besoin.

### 3. Migrer et créer le superadmin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Configurer l'app Web (onglet "Web")

- **Nom** : ton subdomain (ex. `slimani.pythonanywhere.com`).
- **Code > Répertoire de travail (Working directory)** :
  `/home/VOTRE_USER/slimanifarid.github.io`
- **Code > Script de démarrage WSGI** :
  `/home/VOTRE_USER/slimanifarid.github.io/pa_wsgi.py`
- **Ouvre le fichier WSGI** et remplace **tous** les `VOTRE_USER` par ton nom d'utilisateur PythonAnywhere.
- **Virtualenv** : `/home/VOTRE_USER/.virtualenvs/djangoblog`

### 5. Fichiers statiques

Dans la console bash :

```bash
python manage.py collectstatic --noinput
```

Puis dans l'onglet **Web**, rubrique **Static files** :

| URL         | Répertoire                                    |
|-------------|-----------------------------------------------|
| `/static/`  | `/home/VOTRE_USER/slimanifarid.github.io/staticfiles` |
| `/media/`   | `/home/VOTRE_USER/slimanifarid.github.io/media`       |

### 6. Mettre à jour ALLOWED_HOSTS (important)

Le WSGI met `DJANGO_ALLOWED_HOSTS` à `VOTRE_USER.pythonanywhere.com`. Remplace `VOTRE_USER` par ton vrai nom d'utilisateur.

### 7. Redémarrer

Bouton **Reload** en haut de l'onglet Web. Le blog est en ligne sur :
`https://VOTRE_USER.pythonanywhere.com/`

---

## Mettre à jour le code (après une modif locale + push)

```bash
cd /home/VOTRE_USER/slimanifarid.github.io
git pull origin django_blog
python manage.py collectstatic --noinput   # si statiques modifiées
# bouton Reload
```

> SQLite (`db.sqlite3`) est ignoré par git : les articles créés en production restent sur le serveur. Ne jamais `git reset --hard` sans sauvegarder la base.