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
