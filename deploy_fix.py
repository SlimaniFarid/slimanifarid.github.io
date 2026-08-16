#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tout-faire : applique les fichiers Django dans l'ancien dossier du projet
pour que le blog fonctionne dans le projet existant (sans creer de nouveau
projet). A executer SUR PythonAnywhere (console bash) :
    python3.12 deploy_fix.py

Fait :
  1. Copie config/, blog/, templates/, static/, manage.py, requirements.txt,
     pa_wsgi.py, .gitignore depuis le nouveau clone vers l'ancien dossier.
  2. Supprime l'ancien module settings (slimanifarid/).
  3. Corrige les chemins dans pa_wsgi.py.
  4. Migre la base et collecte les statiques.
  5. Ecrit la config WSGI pour l'app web (si possible) + affiche les etapes.
"""
import os
import shutil
import subprocess
import sys

USER = "slimanifarid"
NEW_DIR = f"/home/{USER}/slimanifarid.github.io"     # nouveau clone (source)
OLD_DIR = f"/home/{USER}/slimanifarid"               # ancien dossier (cible)
VENV_PY = f"/home/{USER}/.virtualenvs/djangoblog/bin/python"
WSGI_TARGET = f"/var/www/{USER}_pythonanywhere_com_wsgi.py"

ITEMS = ["config", "blog", "templates", "static", "manage.py",
         "requirements.txt", "pa_wsgi.py", ".gitignore"]


def run(cmd, cwd):
    print("\n>>> " + " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    if not os.path.exists(NEW_DIR):
        print("ERREUR: source introuvable:", NEW_DIR, file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(OLD_DIR):
        print("ERREUR: cible introuvable:", OLD_DIR, file=sys.stderr)
        sys.exit(1)

    print("1/5 - Copie des fichiers Django vers", OLD_DIR)
    for item in ITEMS:
        src = os.path.join(NEW_DIR, item)
        dst = os.path.join(OLD_DIR, item)
        if not os.path.exists(src):
            print("   (absent, ignore) ", item)
            continue
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        print("   copie          ", item)

    print("2/5 - Suppression de l'ancien module settings (slimanifarid/)")
    old_module = os.path.join(OLD_DIR, "slimanifarid")
    if os.path.isdir(old_module):
        shutil.rmtree(old_module)
        print("   supprime       slimanifarid/")
    else:
        print("   rien a faire")

    print("3/5 - Correction des chemins dans pa_wsgi.py")
    wsgi_path = os.path.join(OLD_DIR, "pa_wsgi.py")
    with open(wsgi_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(NEW_DIR, OLD_DIR)
    content = content.replace("VOTRE_USER", USER)
    with open(wsgi_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("   pa_wsgi.py pointe maintenant sur", OLD_DIR, "et user =", USER)

    print("4/5 - Migrations + statiques (venv djangoblog)")
    if os.path.exists(VENV_PY):
        run([VENV_PY, "manage.py", "migrate"], cwd=OLD_DIR)
        run([VENV_PY, "manage.py", "collectstatic", "--noinput"], cwd=OLD_DIR)
    else:
        print("   VENV introuvable:", VENV_PY)
        print("   -> pip install -r requirements.txt puis relancer le script")

    print("5/5 - Ecriture de la configuration WSGI de l'app web")
    try:
        with open(wsgi_path, "r", encoding="utf-8") as f:
            content = f.read()
        os.makedirs("/var/www", exist_ok=True)
        with open(WSGI_TARGET, "w", encoding="utf-8") as f:
            f.write(content)
        print("   -> config WSGI ecrite dans", WSGI_TARGET)
    except Exception as exc:
        print("   Impossible d'ecrire dans /var/www:", exc)
        print("   -> colle ce contenu dans l'onglet Web > WSGI :")
        print("-" * 60)
        print(content)
        print("-" * 60)

    print("\n=== TERMINE ===")
    print("""Dernieres etapes a verifier dans l'onglet Web de PythonAnywhere :
1. Working directory : %s
2. Virtualenv        : /home/%s/.virtualenvs/djangoblog
3. Static files      : /static/  -> %s/staticfiles
                       /media/   -> %s/media
4. Bouton Reload
5. Tester : https://%s.pythonanywhere.com/  et  /admin/
""" % (OLD_DIR, USER, OLD_DIR, OLD_DIR, USER))


if __name__ == "__main__":
    main()
