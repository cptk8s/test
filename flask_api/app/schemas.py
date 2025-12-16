from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Comercial, Cliente, TipoActividad, Actividad


class ComercialSchema(SQLAlchemySchema):
    class Meta:
        model = Comercial
        load_instance = True

    id = auto_field()
    nombre = auto_field()
    apellidos = auto_field()


class ClienteSchema(SQLAlchemySchema):
    class Meta:
        model = Cliente
        load_instance = True

    id = auto_field()
    nombre = auto_field()


class TipoActividadSchema(SQLAlchemySchema):
    class Meta:
        model = TipoActividad
        load_instance = True

    id = auto_field()
    descripcion = auto_field()


class ActividadSchema(SQLAlchemySchema):
    class Meta:
        model = Actividad
        load_instance = True

    id = auto_field()
    fecha = auto_field()
    id_tipo_actividad = auto_field()
    id_comercial = auto_field()
    id_cliente = auto_field()
    titulo = auto_field()
    descripcion = auto_field()
