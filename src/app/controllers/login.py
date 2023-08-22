from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.dependencies.auth_dependency import get_current_user
from src.app.dto.schema import TokenSchema, SystemUser, UserOut
from src.app.utils.JwtUtil import JWTUtil

app = APIRouter()


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = db.get(form_data.username, None)
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    # hashed_pass = user['password']
    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password"
    #     )

    return {
        "access_token": JWTUtil.create_access_token(form_data.username),
        "refresh_token": JWTUtil.create_refresh_token(form_data.password),
    }


@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
