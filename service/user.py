from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, new_user):
        return self.dao.create(new_user)

    def update(self, user):
        self.dao.update(user)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)
