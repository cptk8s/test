from . import db
from datetime import datetime


class Comercial(db.Model):
    __tablename__ = 'comerciales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellidos = db.Column(db.String(128), nullable=True)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256), nullable=False, unique=True)


class TipoActividad(db.Model):
    __tablename__ = 'tipos_actividad'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(256), nullable=False, unique=True)


class Actividad(db.Model):
    __tablename__ = 'actividades'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    id_tipo_actividad = db.Column(db.Integer, db.ForeignKey('tipos_actividad.id'), nullable=False)
    id_comercial = db.Column(db.Integer, db.ForeignKey('comerciales.id'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    titulo = db.Column(db.String(256), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    tipo = db.relationship('TipoActividad')
    comercial = db.relationship('Comercial')
    cliente = db.relationship('Cliente')
