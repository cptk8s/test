from flask import Blueprint, request, jsonify, abort
from .models import Comercial, Cliente, TipoActividad, Actividad
from .schemas import ComercialSchema, ClienteSchema, TipoActividadSchema, ActividadSchema
from . import db

api_bp = Blueprint('api', __name__)

# Comerciales
@api_bp.route('/comerciales', methods=['POST'])
def create_comercial():
    data = request.json
    schema = ComercialSchema()
    comercial = schema.load(data, session=db.session)
    db.session.add(comercial)
    db.session.commit()
    return schema.dump(comercial), 201


@api_bp.route('/comerciales/<int:id>', methods=['GET'])
def get_comercial(id):
    comercial = Comercial.query.get_or_404(id)
    return ComercialSchema().dump(comercial)


@api_bp.route('/comerciales', methods=['GET'])
def list_comerciales():
    args = request.args
    q = Comercial.query
    if 'nombre' in args:
        q = q.filter_by(nombre=args['nombre'])
    items = q.all()
    return jsonify(ComercialSchema(many=True).dump(items))


@api_bp.route('/comerciales/<int:id>', methods=['PUT'])
def update_comercial(id):
    comercial = Comercial.query.get_or_404(id)
    data = request.json
    for k, v in data.items():
        setattr(comercial, k, v)
    db.session.commit()
    return ComercialSchema().dump(comercial)


@api_bp.route('/comerciales/<int:id>', methods=['DELETE'])
def delete_comercial(id):
    comercial = Comercial.query.get_or_404(id)
    db.session.delete(comercial)
    db.session.commit()
    return '', 204

# Clientes
@api_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    schema = ClienteSchema()
    cliente = schema.load(data, session=db.session)
    db.session.add(cliente)
    db.session.commit()
    return schema.dump(cliente), 201


@api_bp.route('/clientes', methods=['GET'])
def list_clientes():
    args = request.args
    q = Cliente.query
    if 'nombre' in args:
        q = q.filter_by(nombre=args['nombre'])
    items = q.all()
    return jsonify(ClienteSchema(many=True).dump(items))


@api_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return ClienteSchema().dump(cliente)

# Tipo de actividad
@api_bp.route('/tipos_actividad', methods=['POST'])
def create_tipo():
    data = request.json
    schema = TipoActividadSchema()
    tipo = schema.load(data, session=db.session)
    db.session.add(tipo)
    db.session.commit()
    return schema.dump(tipo), 201


@api_bp.route('/tipos_actividad', methods=['GET'])
def list_tipos():
    args = request.args
    q = TipoActividad.query
    if 'descripcion' in args:
        q = q.filter_by(descripcion=args['descripcion'])
    items = q.all()
    return jsonify(TipoActividadSchema(many=True).dump(items))


@api_bp.route('/tipos_actividad/<int:id>', methods=['GET'])
def get_tipo(id):
    tipo = TipoActividad.query.get_or_404(id)
    return TipoActividadSchema().dump(tipo)

# Actividades
@api_bp.route('/actividades', methods=['POST'])
def create_actividad():
    data = request.json
    schema = ActividadSchema()
    actividad = schema.load(data, session=db.session)
    db.session.add(actividad)
    db.session.commit()
    return schema.dump(actividad), 201


@api_bp.route('/actividades', methods=['GET'])
def list_actividades():
    items = Actividad.query.all()
    return jsonify(ActividadSchema(many=True).dump(items))


@api_bp.route('/actividades/<int:id>', methods=['GET'])
def get_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    return ActividadSchema().dump(actividad)


@api_bp.route('/actividades/<int:id>', methods=['PUT'])
def update_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    data = request.json
    for k, v in data.items():
        setattr(actividad, k, v)
    db.session.commit()
    return ActividadSchema().dump(actividad)


@api_bp.route('/actividades/<int:id>', methods=['DELETE'])
def delete_actividad(id):
    actividad = Actividad.query.get_or_404(id)
    db.session.delete(actividad)
    db.session.commit()
    return '', 204
