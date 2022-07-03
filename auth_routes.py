from fastapi import APIRouter, HTTPException, status
from werkzeug.security import check_password_hash, generate_password_hash

from database import Session, engine
from models import User
from schemas import SignUpModel

auth_router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

session=Session(bind=engine)

@auth_router.get('/')
async def hello():
    return {'hello': 'world'}

@auth_router.post('/signup', 
    status_code=status.HTTP_201_CREATED
)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    db_username = session.query(User).filter(User.username==user.username).first()

    if db_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)

    session.commit()

    return new_user
