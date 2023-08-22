from uuid import uuid4

from fastapi import APIRouter

from src.app.dto.schema import UserAuth, UserOut
from src.app.utils.JwtUtil import JWTUtil

router = APIRouter()


@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    # user = db.get(data.email, None)
    # if user is not None:
    #         raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exist"
    #     )
    user = {
        'email': data.email,
        'password': JWTUtil.get_hashed_password(data.password),
        'id': str(uuid4())
    }
    # db[data.email] = user    # saving user to database
    return user
