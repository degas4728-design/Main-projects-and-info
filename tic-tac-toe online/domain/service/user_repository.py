class UserRepository:
    def save(self, user):
        raise NotImplementedError

    def find_by_login(self, login: str):
        raise NotImplementedError

    def find_by_id(self, user_id):
        raise NotImplementedError