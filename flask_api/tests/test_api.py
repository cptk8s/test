import json
import pytest
from app import create_app, db

@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(tmp_path / 'test.db')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_crud_client_comercial_and_activity(client):
    # create comercial
    r = client.post('/comerciales', json={'nombre': 'Juan', 'apellidos': 'Perez'})
    assert r.status_code == 201
    comercial = r.get_json()

    # create cliente
    r = client.post('/clientes', json={'nombre': 'Acme'})
    assert r.status_code == 201
    cliente = r.get_json()

    # create tipo actividad
    r = client.post('/tipos_actividad', json={'descripcion': 'Llamada'})
    assert r.status_code == 201
    tipo = r.get_json()

    # create actividad
    payload = {
        'fecha': '2025-12-16T00:00:00',
        'id_tipo_actividad': tipo['id'],
        'id_comercial': comercial['id'],
        'id_cliente': cliente['id'],
        'titulo': 'Primera',
        'descripcion': 'Descripcion'
    }
    r = client.post('/actividades', json=payload)
    assert r.status_code == 201
    actividad = r.get_json()

    # get actividad
    r = client.get(f"/actividades/{actividad['id']}")
    assert r.status_code == 200
    data = r.get_json()
    assert data['titulo'] == 'Primera'
