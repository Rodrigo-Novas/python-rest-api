from flask_marshmallow import Marshmallow

ma = Marshmallow()

# esquema de usuario

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "usuario", "clave")



class PeliculaSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "estreno", "director", "reparto", "genero", "sinopsis")

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "usuario", "clave")


pelicula_schema = PeliculaSchema()
peliculas_schema = PeliculaSchema(many=True)
usuarios_schema = UsuarioSchema(many=True)
