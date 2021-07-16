from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import create_access_token
from models.models import Usuario, Pelicula, db
from schemas.schemas import peliculas_schema, pelicula_schema, usuarios_schema
import bcrypt
blue_print = Blueprint("app", __name__)  # importante el blueprint debe contener si o si nombre de la app y nombre del modulo

# Ruta de inicio


@blue_print.route("/", methods=["GET"])
def init():
    return jsonify(respuesta="Rest API con Python Flask y mysql"), 200


@blue_print.route("/", methods=["POST"])
def registrar_usuario():
    try:
        # obtener datos de la tabla
        usuario = request.json.get("usuario")
        clave = request.json.get("clave")
        if not usuario or not clave:
            return jsonify(respuesta="Campos invalidos"), 400
        # existe usuario
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()
        if existe_usuario:
            return jsonify(respuesta="Usuario ya existe")
        else:
            # Encriptamos clave del usuario
            clave_encriptada = bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt())

            # creamos el modelo
            nuevo_usuario = Usuario(usuario, clave_encriptada)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify(respuesta="Usuario nuevo fue creado satisfactoriamente"), 201
    except Exception as e:
        print(str(e))
        return jsonify(respuesta="Error en peticion"), 500


@blue_print.route("/auth/loguin", methods=["POST"])
def iniciar_sesion():
    try:
        # obtener datos de la tabla
        usuario = request.json.get("usuario")
        clave = request.json.get("clave")
        if not usuario or not clave:
            return jsonify(respuesta="Campos invalidos"), 400
        # existe usuario
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()
        if not existe_usuario:
            return jsonify(respuesta="Usuario no encontrado"), 400
        es_clave_valida = bcrypt.checkpw(clave.encode("utf-8"), existe_usuario.clave.encode("utf-8"))
        if es_clave_valida:
            access_token = create_access_token(identity=usuario)  # creo access token
            return jsonify(access_token=access_token), 200
        return jsonify(respuesa="Clave o usuario incorrecto"), 404
    except Exception:
        return jsonify(respuesta="Error en Peticion"), 500

@blue_print.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    usuario = Usuario.query.with_entities(Usuario.usuario).all()
    if usuario:
        usuarios_json = usuarios_schema.dump(usuario)
        return jsonify(usuarios_json), 200
    else:
        return jsonify(respuesta="No hay usuarios"), 404

# RUTAS PROTEGIDAS POR JWT

# Ruta - Crear pelicula


@blue_print.route("/api/", methods=["POST"])
@jwt_required()
def crear_pelicula():
    try:
        nombre = request.json["nombre"]
        estreno = request.json["estreno"]
        director = request.json["director"]
        reparto = request.json["reparto"]
        genero = request.json["genero"]
        sinopsis = request.json["sinopsis"]

        nueva_pelicula = Pelicula(nombre, estreno, director, reparto, genero, sinopsis)
        db.session.add(nueva_pelicula)
        db.session.commit()

        return jsonify(respuesta="Pelicula almacenada exitosamente"), 201
    except Exception:
        return jsonify(respuesta="Error en peticion"), 500


@blue_print.route("/api/peliculas/", methods=["GET"])
@jwt_required()
def obtener_peliculas():
    try:
        peliculas = Pelicula.query.all()
        respuesta = peliculas_schema.dump(peliculas)  # lo serializo para que quede en formato json
        return jsonify(respuesta), 200
    except Exception:
        return jsonify(respuesta="Error en peticion"), 500


@blue_print.route("/api/pelicula/<int:id>", methods=["GET"])
@jwt_required()
def obtener_pelicula(id):
    try:
        peliculas = Pelicula.query.filter_by(id=id).first()
        respuesta = pelicula_schema.dump(peliculas)  # lo serializo para que quede en formato json
        return jsonify(respuesta), 200
    except Exception:
        return jsonify(respuesta="Error en peticion"), 500


@blue_print.route("/api/pelicula/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_pelicula(id):
    try:
        peliculas = Pelicula.query.filter_by(id=id).first()
        if peliculas:
            peliculas.nombre = request.json["nombre"]
            peliculas.estreno = request.json["estreno"]
            peliculas.director = request.json["director"]
            peliculas.reparto = request.json["reparto"]
            peliculas.genero = request.json["genero"]
            peliculas.sinopsis = request.json["sinopsis"]
            db.session.commit()
            return jsonify(respuesta="la pelicula ha sido cambiada"), 200
        else:
            return jsonify(respuesta="La pelicula es inexistente"), 404
    except Exception as e:
        print(e)
        return jsonify(respuesta="Error en peticion"), 500


@blue_print.route("/api/pelicula/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_pelicula(id):
    try:
        peliculas = Pelicula.query.filter_by(id=id).first()
        if peliculas:
            db.session.delete(peliculas)
            db.session.commit()
            return jsonify(respuesta="Pelicula eliminada correctamente"), 200
        else:
            return jsonify(respuesta="No se encontro la pelicula"), 404
    except Exception:
        return jsonify(respuesta="Error en peticion"), 500
