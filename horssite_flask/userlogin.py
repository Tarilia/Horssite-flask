from flask_login import UserMixin

from horssite_flask.database import get_user


class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])
