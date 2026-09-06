from datasource.model.storage import DataUser
from domain.model.user import User

class UserMapper:
    @staticmethod
    def domain_to_storage(user: User) -> DataUser:
        return DataUser(
            id=user.id,
            login=user.login,
            password=user.password
        )

    @staticmethod
    def storage_to_domain(data_user: DataUser) -> User:
        return User(
            user_id=data_user.id,
            login=data_user.login,
            password=data_user.password
        )