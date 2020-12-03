import os
import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
# from models import db, User, Category
from models.users import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql://ub5z2hnzlwc5frzq:Tlut4m6TTQDFybjxyeMs@bodwcrfuz4icrcbxrqjn-mysql.services.clever-cloud.com:3306/bodwcrfuz4icrcbxrqjn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SECRET KEY"] = "secret key"
app.config["JWT_SECRET_KEY"] = "encrypt"

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
        password_hash = bcrypt.generate_password_hash(request.json.get("userPass"))
        _userPass = password_hash
    else:
        return jsonify({"msg": "El formato de la contraseña no es valido"}), 401
    
    _userName = request.json.get("userName")
    _firstName = request.json.get("firstName")
    _lastName = request.json.get("lastName")
    _isAdmin = request.json.get("isAdmin")
    _bio = 'No bio'

    User.add_user(_firstName, _lastName, _email, _userName, _userPass, _bio, _isAdmin)

    return jsonify({"success": True})



@app.route('/users', methods=["GET"])
def get_all_users():
    return jsonify({"Users": User.get_all_users()})

@app.route('/users/<int:id>', methods=["GET"])
def get_user_by_id(id):
    user = User.get_user(id)
    return jsonify(user)

# @app.route('/user/<int:id>',methods["GET", "DELETE","PUT"])
# @app.route('/user',methods=["POST","GET"])
# def user(id=None):
#     if id is not None:
#         if request.method == 'GET':
#             user= User.query.all()
#             return jsonify(user.serialize()), 200

#     if request.method == 'PUT':
#         user = User.query.get(id)
#         user.bio = request.json.get("bio")
#         db.session.commit()
#         return jsonify({"msg": "User updated"}), 200
    
#     if request.method == 'DELETE':
#         user = User.query.get(id)
#         db.session.delete(user)
#         db.session.commit()


#         return jsonify({"msg": "User deleted"}), 200

#     elif request.method == 'POST':
#         user = User()
#         user.name = request.json.get("name")
#         user.email = request.json.get("email")
#         user.password = request.json.get("password")
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(user,serialize()), 200

#     else:
#         users = User.query.all()
#         users = list(map(lambda category:users.serialize(), categories))
#         return jsonify({"users":users}), 200


    if __name__ == "__main__":
        manager.run()
    
    

        







