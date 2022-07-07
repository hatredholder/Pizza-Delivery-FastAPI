from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User
from sqlalchemy.orm import Session


def jwt_required(Authorize: AuthJWT):
    """
        JWT Authentication from the fastapi_jwt_auth module
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

def get_current_user(Authorize: AuthJWT, session: Session):
    """
        Returns JWT authorized user model
    """
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return user
