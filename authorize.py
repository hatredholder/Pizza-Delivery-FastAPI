from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT


def jwt_required(Authorize: AuthJWT = Depends()):
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
