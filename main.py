from fastapi import FastAPI
from .app import app
from .app.middleware import JWTMiddleware
from .app.database import init_db
from .app.api import users

exempt_routes = ["/api/users/", "/api/login"]  # Rutas que no requieren autenticación

app.add_middleware(JWTMiddleware, exempt_routes=exempt_routes)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)