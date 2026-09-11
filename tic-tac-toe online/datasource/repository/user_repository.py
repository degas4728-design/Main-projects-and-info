from domain.service.user_repository import UserRepository
from datasource.database import SessionLocal
from datasource.model.storage import DataUser

class UserRepositoryImpl(UserRepository):
    def save(self, user):
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.close()

    def find_by_login(self, login: str):
        db = SessionLocal()
        user = db.query(DataUser).filter(DataUser.login == login).first()
        db.close()
        return user

    def find_by_id(self, user_id):
        db = SessionLocal()
        user = db.query(DataUser).filter(DataUser.id == user_id).first()
        db.close()
        return user