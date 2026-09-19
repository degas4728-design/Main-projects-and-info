from  fastapi import FastAPI
from  ..Model.domain.aut_service import auth_service
from pydantic import BaseModel

app = FastAPI()


@app.post("/registrations/{login, password}")
def registration(login: str,password: str ):
    return auth_service.registration(login, password)

@app.post("/authorization")
def authorization():
    pass

# @app.get("/")
# @authorization
# def connect(request: Request):
#     return 200


