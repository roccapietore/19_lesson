from flask import request
from flask_restx import Resource, Namespace, abort

from marshmallow import Schema, fields, ValidationError
from implemented import auth_service

auth_ns = Namespace('auth')


class AuthValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        try:
            data = AuthValidator().load(req_json)
            tokens = auth_service.get_tokens(data)
            return tokens, 201
        except ValidationError:
            abort(404)

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(404)
        tokens = auth_service.get_refresh_token(refresh_token)
        return tokens, 201

