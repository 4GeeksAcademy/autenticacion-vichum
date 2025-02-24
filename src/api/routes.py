from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from api.models import db, User
from api.utils import APIException
import bcrypt

api = Blueprint("api", __name__)
CORS(api)

@api.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Todos los campos deben estar completos"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify({"message": "Correo o contraseña incorrectos"}), 400

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.serialize()}), 200

@api.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Todos los campos deben estar completos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "El usuario ya existe"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

    new_user = User(email=email, password=hashed_password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente", "user": new_user.serialize()}), 201
