import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

SECRET_KEY = "your_secret_key"

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_routes=None):
        super().__init__(app)
        self.security = HTTPBearer()
        self.exempt_routes = exempt_routes if exempt_routes is not None else []

    async def dispatch(self, request: Request, call_next):
        print(request.url.path)
        if request.url.path in self.exempt_routes:
            return await call_next(request)

        if "Authorization" not in request.headers:
            return JSONResponse(status_code=403, content={"detail": "Authorization header missing"})

        credentials: HTTPAuthorizationCredentials = await self.security(request)
        token = credentials.credentials

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token has expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        response = await call_next(request)
        return response