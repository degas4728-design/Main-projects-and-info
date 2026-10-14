from ..database.database import create_user, get_hash_db
class UserService():

    @staticmethod
    async def add_user(new_user):
        await create_user(new_user)

    @staticmethod
    async def get_hash_us(login):
        return await get_hash_db(login)
