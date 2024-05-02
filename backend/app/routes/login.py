#login for the first time, token generate

from datetime import datetime, timedelta, timezone
from typing import Annotated
from schema import User, Token, TokenData
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError
import jwt
from passlib.context import CryptContext
from config import conn



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cursor = conn.cursor()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

log = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    # print("\n\n\n\nrow = ", row, "\n\n\n\n")
    if row:
        user_id, username, email, password, created_at = row
        user_dict = {'username': username, 'password': password, 'created_at': created_at}
        print("result:  ",user_dict)
        return User(**user_dict)
    else:
        return None


def authenticate_user(username: str, password: str):
    print(username)
    a = get_user(username)
    print('\n\n\nauthenticated_user = ', a,"\n\n\n")
    return a
    # user = get_user(fake_db, username)
    # if not user:
    #     return False
    # if not verify_password(password, user.hashed_password):
    #     return False
    # return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print("\n\n\nto_encode = ", to_encode, "\n\n\n")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload= ", payload,"\n")

        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except HTTPException:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    print("\n\n\n= current user", current_user,"\n\n")
    return current_user

@log.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    
    user = authenticate_user(form_data.username, form_data.password)
    print("\n\n\n\nuser = ", user, "\n\n\n")
   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #print("\n\n\n\nuser = ", user, "\n\n\n")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email}
    )
    
    return Token(access_token=access_token, token_type="bearer")




@log.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)], ):
    return current_user


@log.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]