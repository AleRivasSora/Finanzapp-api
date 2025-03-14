import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.database import get_session
from app.models import User, Categories
from app.schemas import UserCreate, UserRead, UserLogin, UserReadAllData
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils import popDate
import os
from app.middleware import SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        statement = select(User).where(User.email == email, User.deleted_at.is_(None))
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@router.post("/register", response_model=UserRead, tags=["users"])
def register(user: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password, created_at=datetime.now(), updated_at=datetime.now())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user_dict = popDate(db_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User registered successfully", "user": user_dict})

@router.post("/login", response_model=UserRead, tags=["users"])
def login(user: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Login successful", "access_token": access_token, "token_type": "bearer"})

@router.get("/me", response_model=UserReadAllData, tags=["users"], status_code=status.HTTP_200_OK)
def current_user(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(User).where(User.id == current_user.id)
    user = session.exec(statement).first()
    initial_categories = session.exec(select(Categories).where(Categories.is_initial == 1)).all()
    user_categories = session.exec(select(Categories).where(Categories.user_id == current_user.id)).all()
    all_categories = list(initial_categories) + list(user_categories)
    user_all_data = User(**user.__dict__, categories=all_categories)
    if user_all_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_all_data