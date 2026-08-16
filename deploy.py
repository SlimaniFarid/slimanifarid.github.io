#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploiement semi-auto du blog Django (branche django_blog) sur PythonAnywhere.
A executer dans la console Bash PythonAnywhere depuis n'importe quel dossier :
    python3.12 deploy.py
Le projet est clone sur PythonAnywhere dans ~/slimanifarid.github.io (l'ancien
projet dans ~/slimanifarid n'est pas touche).
"""
import os
import shutil
import subprocess
import sys

USERNAME = "slimanifarid"
GITHUB_REPO = "https://github.com/SlimaniFarid/slimanifarid.github.io.git"
BRANCH = "django_blog"
PYTHON = "python3.12"
WEBAPP = f"{USERNAME}.pythonanywhere.com"

HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME, "slimanifarid.github.io")
VENV_DIR = os.path.join(HOME, ".virtualenvs", "djangoblog")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
VENV_PIP = os.path.join(VENV_DIR, "bin", "pip")


def log(msg):
    print("\n=== " + msg + " ===", flush=True)


def check(cmd, cwd=None):
    print("> " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)
    return True


def main():
    log("Configuration")
    print(f"Utilisateur    : {USERNAME}")
    print(f"Projet         : {PROJECT_DIR}")
    print(f"Virtualenv     : {VENV_DIR}")
    print(f"App web        : https://{WEBAPP}/")

    log("1/4 - Recuperation du code (branche " + BRANCH + ")")
    if os.path.exists(os.path.join(PROJECT_DIR, "manage.py")):
        check(["git", "pull", "origin", BRANCH], cwd=PROJECT_DIR)
    else:
        parent = os.path.dirname(PROJECT_DIR)
        if os.path.exists(PROJECT_DIR):
            shutil.rmtree(PROJECT_DIR)
        check(["git", "clone", "-b", BRANCH, GITHUB_REPO, PROJECT_DIR])

    log("2/4 - Remplacement de VOTRE_USER dans pa_wsgi.py et README.md")
    for name in ("pa_wsgi.py", "README.md"):
        path = os.path.join(PROJECT_DIR, name)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("VOTRE_USER", USERNAME)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"-> {name} : VOTRE_USER -> {USERNAME}")

    log("3/4 - Virtualenv + dependances")
    if not os.path.exists(VENV_PYTHON):
        parent = os.path.dirname(VENV_DIR)
        os.makedirs(parent, exist_ok=True)
        check([PYTHON, "-m", "venv", VENV_DIR])
    check([VENV_PIP, "install", "--upgrade", "pip"])
    check([VENV_PIP, "install", "-r", os.path.join(PROJECT_DIR, "requirements.txt")])

    log("4/4 - Migrations + superuser + statiques")
    check([VENV_PYTHON, "manage.py", "migrate"], cwd=PROJECT_DIR)
    print("\nCreation / verification du superadmin (creer-un au premier deploiement).")
    check([VENV_PYTHON, "manage.py", "createsuperuser"], cwd=PROJECT_DIR)
    check([VENV_PYTHON, "manage.py", "collectstatic", "--noinput"], cwd=PROJECT_DIR)

    log("DEPLOIEMENT DU CODE TERMINE")
    print("""
A configurer ensuite dans l'onglet Web de PythonAnywhere (a la main) :

1. Nom de l'app : {webapp}
2. Onglet Code :
   - Working directory      : {proj}
   - Script de demarrage WSGI : {proj}/pa_wsgi.py
3. Virtualenv               : {venv}
4. Onglet Static files :
   /static/  -> {proj}/staticfiles
   /media/   -> {proj}/media
5. Bouton Reload

Puis test sur https://{webapp}/  et  https://{webapp}/admin/
""".format(webapp=WEBAPP, proj=PROJECT_DIR, venv=VENV_DIR))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print("\nERREUR : la commande a echoue -> " + " ".join(exc.cmd), file=sys.stderr)
        sys.exit(1)