from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer

app=FastAPI()
outh2_scheme=OAuth2PasswordBearer(tokenUrl="token")
#The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

@app.get("/items/")
async def read_items(token:str=Depends(outh2_scheme)):
    return {"token":token}