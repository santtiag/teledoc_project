import sys
import os

# Añadir el directorio actual al path de Python
INTERP = os.path.expanduser("/home/teledoc1/web_teledoc/teledoc_project/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

# Importar tu aplicación FastAPI
from main import app

# Crear la aplicación WSGI
from fastapi.middleware.wsgi import WSGIMiddleware

application = WSGIMiddleware(app)
