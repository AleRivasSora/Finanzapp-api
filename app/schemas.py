from sqlmodel import SQLModel , Field
from pydantic import EmailStr, BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List


###################### User ######################
class UserBase(SQLModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode: True

class UserLogin(SQLModel):
    email: EmailStr
    password: str


###################### Budget ######################

class BudgetBase(SQLModel):
    name: str
    amount: float
    

class BudgetCreate(BudgetBase):
   pass

class BudgetRead(BudgetBase):
    id: UUID
    message: Optional[str] = None
    initial_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: True

class BudgetListResponse(SQLModel): 
    data: List[BudgetRead]  

    class Config:
        orm_mode = True
    
class BudgetUpdate(BudgetBase):
    pass

###################### UserReadAllData ######################

class UserReadAllData(BaseModel):  
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    categories: List["CategoryRead"]     

    class Config:
        orm_mode = True


###################### Category ######################
class CategoryRead(BaseModel):
    id: UUID
    name: str
    is_initial: bool
    user_id: Optional[int]

    class Config:
        orm_mode = True


############# Transaction #####################

class TransactionBase(BaseModel): 
    amount: float
    description: Optional[str] = None
    budget_id: UUID

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    budget_id: Optional[UUID] = None
    user_id: int 

    class Config:
        orm_mode = True

class TransactionUpdate(BaseModel): 
    amount: Optional[float] = None
    description: Optional[str] = None
    budget_id: Optional[UUID] = None

class TransactionListResponse(BaseModel):  
    data: List[TransactionRead]

    class Config:
        orm_mode = True