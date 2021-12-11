import base64
import hashlib
import hmac
import jwt
import calendar
import datetime
from constants import secret, algo
from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user):
        user["password"] = self.get_hash(user.get("password"))
        return self.dao.create(user)

    def update(self, user):
        user["password"] = self.get_hash(user.get("password"))
        self.dao.update(user)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)
        return base64.b85encode(hash_digest)

    def compare_passwords(self, password_hash, other_password):
        return hmac.compare_digest(
            base64.b85decode(password_hash),
            hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS))

    def user_by_username(self, username):
        user = self.dao.user_by_username(username)
        if user is None:
            return {"error": "Неверные учётные данные"}, 401
        return user

    def get_tokens(self, data):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

