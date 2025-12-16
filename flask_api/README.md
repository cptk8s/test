# Flask API for Comerciales, Clientes, Tipos de Actividad y Actividades

Endpoints:
- /comerciales
- /clientes
- /tipos_actividad
- /actividades

Run locally:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py

Run tests:

pytest

Docker:

docker build -t myflaskapi:latest .
docker run -p 5000:5000 myflaskapi:latest

Notes: uses SQLite by default. The API is minimal and intended as a starting point.
