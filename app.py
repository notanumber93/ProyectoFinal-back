from models import *
import datetime
import os
import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://ub5z2hnzlwc5frzq:Tlut4m6TTQDFybjxyeMs@bodwcrfuz4icrcbxrqjn-mysql.services.clever-cloud.com:3306/bodwcrfuz4icrcbxrqjn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SECRET KEY"] = "secret key"
app.config["JWT_SECRET_KEY"] = "4jk132l8x76c4vb079sd8fg"
db = SQLAlchemy(app)

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

@app.route('/signup', methods=["POST"])
def signup():
    email_reg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    password_reg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

    if re.search(email_reg, request.json.get("email")):
        _email = request.json.get("email")
    else:
        return jsonify({"msg": "Este correo no tiene formato valido"}), 401

    if re.search(password_reg, request.json.get("userPass")):
        password_hash = bcrypt.generate_password_hash(
            request.json.get("userPass"))
        _userPass = password_hash
    else:
        return jsonify({"msg": "El formato de la contraseña no es valido"}), 401

    _userName = request.json.get("userName")
    _firstName = request.json.get("firstName")
    _lastName = request.json.get("lastName")
    _isAdmin = request.json.get("isAdmin")
    _bio = 'No bio'

    User.add_user(_firstName, _lastName, _email,
                  _userName, _userPass, _bio, _isAdmin)

    return jsonify({"success": True})


@app.route('/login', methods=["POST"])
def login():
    email_reg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    email = None
    userName = None

    if not request.is_json:
        return jsonify({"msg": "El body o contenido esta vacio"}), 400

    password = request.json.get("userPass", None)

    if not request.json.get("userLogin"):
        return jsonify({"msg": "Falta enviar el nombre de usuario o correo"}), 400

    if not password:
        return jsonify({"msg": "Falta enviar la contraseña"}), 400

    if re.search(email_reg, request.json.get("userLogin")):
        email = request.json.get("userLogin")
        user = User.query.filter_by(email=email).first()
    else:
        userName = request.json.get("userLogin")
        user = User.query.filter_by(userName=userName).first()

    if not user:
        return jsonify({"msg": "Este usuario no esta registrado"}), 404

    identity = user.email
    expires = datetime.timedelta(days=7)

    if bcrypt.check_password_hash(user.userPass, password):
        access_token = create_access_token(
            identity=identity, expires_delta=expires)
        return jsonify({
            "access_token": access_token,
            "user": user.serialize(),
            "success": True
        }), 200
    else:
        return jsonify({"msg": "Contraseña erronea"}), 400


@app.route('/users', methods=["GET"])
@jwt_required
def get_all_users():
    return jsonify({"Users": User.get_all_users()})


@app.route('/users/<int:id>', methods=["GET"])
@jwt_required
def get_user_by_id(id):
    user = User.get_user(id)
    return jsonify(user)


@app.route('/users/<int:id>', methods=["PUT"])
@jwt_required
def update_user(id):
    email_reg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    password_reg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

    if request.json.get("email") is not None:
        if re.search(email_reg, request.json.get("email")):
            _email = request.json.get("email")
        else:
            return jsonify({"msg": "Este correo no tiene formato valido"}), 401

    if request.json.get("userPass") is not None:
        if re.search(password_reg, request.json.get("userPass")):
            password_hash = bcrypt.generate_password_hash(
                request.json.get("userPass"))
            _userPass = password_hash
        else:
            return jsonify({"msg": "El formato de la contraseña no es valido"}), 401

    _email = request.json.get(
        "email") if not request.json.get("email") else _email
    _userPass = request.json.get("userPass") if not request.json.get(
        "userPass") else _userPass
    _userName = request.json.get("userName", None)
    _firstName = request.json.get("firstName", None)
    _lastName = request.json.get("lastName", None)
    _bio = request.json.get("bio", None)
    _isAdmin = request.json.get("isAdmin", None)

    User.update_user(id, _firstName, _lastName, _email,
                     _userName, _userPass, _bio, _isAdmin)

    return jsonify({"success": True})


@app.route('/users/<int:id>', methods=["DELETE"])
@jwt_required
def delete_user(id):
    User.delete_user(id)
    return jsonify({"success": True})


@app.route('/api/rate', methods=["POST"])
@jwt_required
def rate_movie():
    if not request.is_json:
        return jsonify({"msg": "El body o contenido esta vacio"}), 400

    rate = Rate()
    rate.user_id = request.json.get("user_id", None)
    rate.movie_id = request.json.get("movie_id", None)
    rate.rate = request.json.get("rate", None)

    db.session.add(rate)
    db.session.commit()

    return jsonify({"msg": "me he guardado exitosamente"})

@app.route('/favorites/<int:id>', methods=["GET"])
@jwt_required
def get_favorites_by_user(id):
    favorites = Favorites.get_favorites(id)
    return jsonify(favorites)

@app.route('/favorites/', methods=["POST"])
@jwt_required
def add_favorites():
    if not request.is_json:
        return jsonify({"msg": "El body o contenido esta vacio"}), 400

    favorites = Favorites()
    favorites.user_id = request.json.get("user_id", None)
    favorites.movie_id = request.json.get("movie_id", None)

    db.session.add(favorites)
    db.session.commit()

    return jsonify({"msg": "Agregado a favoritos exitosamente"})

if __name__ == "__main__":
    manager.run()
