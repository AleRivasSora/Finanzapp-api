from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import JWTMiddleware
from app.database import init_db
from app.api import users
from app.api import budgets
from app.api import transactions
from app.seeders import seed_categories
from sqlmodel import Session
from app.database import engine

app = FastAPI()

# Rutas que no requieren autenticación
exempt_routes = ["/register", "/login", "/docs", "/openapi.json"]

app.add_middleware(JWTMiddleware, exempt_routes=exempt_routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)



@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
        seed_categories(session)

app.include_router(users.router, prefix="")
app.include_router(budgets.router, prefix="")
app.include_router(transactions.router, prefix="")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


### uvicorn main:app --reload
 