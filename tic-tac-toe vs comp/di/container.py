from datasource.repository.repository_impl import Gamerepositoryimpl
from domain.service.service_impl import Gamelogic

class Container():
    def __init__(self):
        self._repo = None
        self._service = None

    def get_repository(self):
        if self._repo is None:
            self._repo = Gamerepositoryimpl()
        return self._repo

    def get_service(self):
        if self._service is None:
            repo = self.get_repository()
            self._service = Gamelogic(repo)
        return self._service