import uuid

class User:
    def __init__(self, login: str, password: str, user_id: uuid.UUID = None):
        self.id = user_id if user_id else uuid.uuid4()
        self.login = login
        self.password = password

        