from  fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from  ..Model.domain.aut_service import auth_service
from pydantic import BaseModel
from ..Model.domain.model import UserSchema

from ..Model.database.database import drop_tables as dt, create_tables as ct
app = FastAPI()

@app.post("/registration")
async def registration(data: UserSchema):
    return await auth_service.registration(data.login, data.password_hash)

@app.post("/authorization")
async def authorization(data: UserSchema):
    result = await auth_service.authorization(data.login, data.password_hash)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": "Неверный логин или пароль"}
            )
    return {"status": True, "message": "Авторизованы"}

@app.delete("/delete")
async def delete_tables():
    return  await dt()

@app.post("/create")
async def create_tables():
    return  await ct()

# @app.get("/")
# @authorization
# def connect(request: Request):
#     return 200


