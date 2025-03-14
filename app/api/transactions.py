from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Budgets, Transaction
from app.api.users import get_current_user
from fastapi.responses import JSONResponse
from app.schemas import TransactionListResponse, TransactionRead, TransactionCreate
import logging

router = APIRouter()

@router.post("/add-transaction", tags=["transactions"], response_model=TransactionRead,status_code=status.HTTP_201_CREATED)
def add_transaction(transaction: TransactionCreate, session: Session = Depends(get_session),user: User = Depends(get_current_user)):
    budget = session.exec(select(Budgets).where(Budgets.id == transaction.budget_id, Budgets.user_id == user.id)).first()

    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found or does not belong to the user")
    session.refresh(budget) 
    
    budget.amount += transaction.amount
    budget.updated_at = datetime.now()

    db_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        budget_id=transaction.budget_id,
        user_id=user.id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    session.add(db_transaction)
    session.add(budget)  
    try:
        session.commit() 
        session.refresh(db_transaction)
        session.refresh(budget)
        return db_transaction
    except Exception as e:
        session.rollback()
        print(f"Error during transaction creation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Transaction creation failed")