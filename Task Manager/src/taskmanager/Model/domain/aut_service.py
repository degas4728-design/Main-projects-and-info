import asyncio
from fastapi import FastAPI
import bcrypt
from .user_service import UserService
from .model import UserSchema

class auth_service():
          
    # @authorization
    @staticmethod 
    async def authorization(login, password):
        password_hash = await UserService.get_hash_us(login) 
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")) 
    
    # @registration
    @staticmethod
    async def registration(login, password):
        # if check_login(login) == False:
        #     raise ValueError("Логин занят")
        password_hash = await bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
        new_user = UserSchema(login=login, password_hash=password_hash)
        await UserService.add_user(new_user)
        