from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def init_db():
    import app.models  
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session