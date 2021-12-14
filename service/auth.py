import jwt
import calendar
import datetime
from flask_restx import abort

from constants import secret, algo
from dao.model.user import User
from service.user import UserService
from setupdb import db


class AuthService:

    @staticmethod
    def get_tokens(data):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    def user_by_username(self, username, password):
        user = db.session.query(User).filter(User.username == username).first()
        if not user or user.password != UserService.get_hash(password):
            return abort(401)

        return self.get_tokens({
            "username": user.username,
            "password": user.password,
            "role": user.role
        })

    def get_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
            return self.get_tokens(data)
        except:
            abort(404)
