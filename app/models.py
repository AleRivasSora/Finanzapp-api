from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4 

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime = Field(default=None, nullable=True)

    categories: list["Categories"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

class Budgets(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    amount: float
    initial_amount: float
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime = Field(default=None, nullable=True)

    transactions: List["Transaction"] = Relationship(back_populates="budget")
    
    def __repr__(self):
        return f"<Budgets(budget_name={self.name}, budget_amount={self.amount})>"

class Categories(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    is_initial: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime = Field(default=None, nullable=True)

    user: Optional["User"] = Relationship(back_populates="categories")

    def __repr__(self):
        return f"<Categories(category_name={self.name})>"
    
class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    budget_id: UUID = Field(foreign_key="budgets.id") 
    amount: float  
    description: Optional[str] = Field(default=None) 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    budget: "Budgets" = Relationship(back_populates="transactions") 
    user: "User" = Relationship(back_populates="transactions")