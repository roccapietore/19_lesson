import jwt
from constants import secret, algo
from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import UserSchema
from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        schema = UserSchema().load(req_json)
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        user = user_service.user_by_username(username)
        verification = user_service.compare_passwords(password_hash=user.password, other_password=password)
        if not verification:
            abort(403)
        data = {
            "username": user.username,
            "role": user.role
        }
        tokens = user_service.get_tokens(data)
        return tokens, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)
        data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        username = data.get("username")
        user = user_service.user_by_username(username)
        data = {
            "username": user.username,
            "role": user.role
        }
        tokens = user_service.get_tokens(data)
        return tokens, 201
