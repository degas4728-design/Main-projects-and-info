from  fastapi import FastAPI, Request
from  ..Web.req_aut import authorization, registration


app = FastAPI()



@app.get("/")
@authorization
def connect(request: Request):
    return 200


