import asyncio
from fastapi import FastAPI
import bcrypt
from .user_service import create_user
from .models import UserSchema

class auth_service():
          
    # @authorization 
    async def authorization():
        pass

    # @registration
    async def registration(login, password):
        if check_name(login) == False:
            raise ValueError("Имя существует")
        password_hash = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
        new_user.login = login
        new_user.password_hash = password_hash
        new_user = UserSchema()
        create_user(new_user)
        
    def check_name(login):
        pass