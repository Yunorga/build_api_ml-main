import secrets
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin"
    },
}

tokens = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(username: str, password: str):

    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

def create_access_token(data: dict) -> str:

    username = data.get("sub")
    if not username:
        raise HTTPException(status_code=400, detail="Username missing")
    token = secrets.token_hex(16)
    tokens[token] = username
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):

    username = tokens.get(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
