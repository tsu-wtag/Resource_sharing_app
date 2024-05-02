#registered user login korbe

from config import conn
from fastapi import APIRouter
from models import generate_token


cursor = conn.cursor()
log = APIRouter()


@log.post("/login")
async def login(username: str, password: str):
    query = "SELECT id, password FROM users WHERE username = %s"

    cursor.execute(query, (username, ))
    row = cursor.fetchone()

    id, password = row
    if password == password:
        return {"msg": "It is an authenticated user."}
    else:
        return None  # Username not found



