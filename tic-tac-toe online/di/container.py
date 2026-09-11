from datasource.repository.game_repository_impl import GameRepositoryImpl
from domain.service.service_impl import Gamelogic
from datasource.repository.user_repository import UserRepositoryImpl
from domain.service.auth_service import AuthService

class Container():
    def __init__(self):
        from datasource.database import init_db
        init_db()
        self._repo = None
        self._service = None

    def get_repository(self):
        if self._repo is None:
            self._repo = GameRepositoryImpl()
        return self._repo

    def get_service(self):
        if self._service is None:
            repo = self.get_repository()
            self._service = Gamelogic(repo)
        return self._service
    
    def get_auth_service(self):
        if not hasattr(self, "_auth_service"):
            self._auth_service = AuthService(UserRepositoryImpl())
        return self._auth_service