from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, new_user):
        ent = User(**new_user)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, updated_user):
        user = self.get_one(updated_user.get("id"))
        user.username = updated_user.get("username")
        user.password = updated_user.get("password")
        user.role = updated_user.get("role")

        self.session.add(user)
        self.session.commit()

    def user_by_username(self, username):
        user = self.session.query(User).filter(User.username == username).first()
        return user
