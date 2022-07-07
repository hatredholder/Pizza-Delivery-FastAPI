import inspect
import re

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi_jwt_auth import AuthJWT

from auth_routes import auth_router
from order_routes import order_router
from schemas import Settings

app = FastAPI()

def custom_openapi():
    """
        Custom JWT Authorization for Swagger UI
        How to use:
        1) Go to /docs/
        2) Press the "Authorize" button
        3) Enter "Bearer YOUR_ACCESS_TOKEN" 
        where YOUR_ACCESS_TOKEN is your JWT access token
        4) Press "Authorize"
        5) You're JWT authorized
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "Pizza Delivery API",
        version = "1.0",
        description = "An API for a Pizza Delivery Service",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@AuthJWT.load_config
def get_config():
    """
        Get Config function for the fastapi_jwt_auth module
        returns Settings which is a pydantic model,
        that has a authjwt_secret_key variable
    """
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)


