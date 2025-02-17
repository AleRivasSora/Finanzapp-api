from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import JWTMiddleware
from app.database import init_db
from app.api import users

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Agrega aquí otros orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas que no requieren autenticación
exempt_routes = ["/register", "/login"]

app.add_middleware(JWTMiddleware, exempt_routes=exempt_routes)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)