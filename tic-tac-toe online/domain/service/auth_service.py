import base64
from domain.model.user import User
from domain.service.user_repository import UserRepository
from datasource.mapper.user_mapper import UserMapper

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def register(self, login: str, password: str) -> bool:
        if self._user_repo.find_by_login(login):
            return False
        user = User(login=login, password=password)
        self._user_repo.save(UserMapper.domain_to_storage(user))
        return True

    def authenticate(self, auth_header: str) -> str | None:
        if not auth_header or not auth_header.startswith("Basic "):
            return None
        encoded = auth_header[6:]
        decoded = base64.b64decode(encoded).decode("utf-8")
        login, password = decoded.split(":", 1)
        data_user = self._user_repo.find_by_login(login)
        if data_user:
            user = UserMapper.storage_to_domain(data_user)
            if user.password == password:
                return str(user.id)
        return None