"""
WSGI d'entree pour PythonAnywhere.

Dans l'onglet Web > Code :
  1. Repertoire de travail (Working directory) :
     /home/VOTRE_USER/slimanifarid.github.io
  2. Script WSGI : /home/VOTRE_USER/slimanifarid.github.io/pa_wsgi.py
  3. Fichier source du code WSGI : ce fichier.
"""
import os
import sys

# Chemin absolu vers le dossier projet (celui qui contient manage.py et config/)
PROJECT_DIR = "/home/VOTRE_USER/slimanifarid.github.io"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_DEBUG", "0")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "VOTRE_USER.pythonanywhere.com")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()