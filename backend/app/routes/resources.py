#login for the first time, token generate

from datetime import datetime, timedelta, timezone
from typing import Annotated
from schema import Resources, Token, TokenData, Resource_details
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError
import jwt
from passlib.context import CryptContext
from config import conn
from routes.login import get_current_active_user, authenticate_user, create_access_token
import psycopg2
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cursor = conn.cursor()
res = APIRouter()

###----print all the resources-----
cursor = conn.cursor()
user = APIRouter()

@res.get("/resources/")
def all_resources():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, user_id, title FROM resources;", )
        resources = cursor.fetchone()
        return {"id": resources[0], "user_id": resources[1], "title": resources[2]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {e}")
    

# @res.post("/resource/new")
# async def insert_new_resource(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
    
#     user = authenticate_user(form_data.username, form_data.password)
   
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     #print("\n\n\n\nuser = ", user, "\n\n\n")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"username": user.username, "email": user.email}
#     )
    
#     return Token(access_token=access_token, token_type="bearer")

