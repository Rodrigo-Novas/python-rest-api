from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from routes.routes import blue_print
from flask_jwt_extended import JWTManager
import datetime




app = Flask(__name__)

# Base de datos
db_usuario = "root"
db_password = "rodrigodatabase"
db_host = "localhost"
# la base de datos o schema que vamos a colocarle al proyecto
db_nombre = "db_api_python"

# connection string
DB_URL = f"mysql+pymysql://{db_usuario}:{db_password}@{db_host}/{db_nombre}"

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "3st4-3s-M1-Cl4ave-Se3cr3ta"  # Coloco secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=12)  # Coloco el tiempo de expiracion del jwt token

# jwt

jwt = JWTManager(app)


# inicializamos SQLAlchemy
db.init_app(app)

# Instanciamos las rutas

app.register_blueprint(blue_print)

# Creamos la Base de datos SI NO EXISTE LA CREA
with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)  # crea bdd
    db.create_all()  # crea todo

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
