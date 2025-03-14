import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Budgets
from app.schemas import BudgetCreate, BudgetRead, BudgetUpdate, BudgetListResponse
from app.api.users import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter()



def get_current_budget(user: User, budget_id: int, session: Session):
    statement = select(Budgets).where(Budgets.id == budget_id, Budgets.user_id == user.id, Budgets.deleted_at.is_(None))
    budget = session.exec(statement).first()
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.post("/create-budget", response_model=BudgetRead, tags=["budgets"], status_code=status.HTTP_201_CREATED)
def create_budget(budget: BudgetCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    statement = select(Budgets).where(Budgets.name == budget.name, Budgets.user_id == user.id, Budgets.deleted_at.is_(None))
    existing_budget = session.exec(statement).first()

    if existing_budget:
        raise HTTPException(status_code=400, detail="Budget name already exists")
    db_budget = Budgets(**budget.dict(), user_id=user.id, initial_amount=budget.amount,created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return BudgetRead(**db_budget.__dict__, message="Budget created successfully")

@router.get("/get-budgets", response_model=BudgetListResponse, tags=["budgets"], status_code=status.HTTP_200_OK)
def get_budgets(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    statement = select(Budgets).where(Budgets.user_id == user.id, Budgets.deleted_at.is_(None))
    budgets = session.exec(statement).all()
    print(budgets)
    print("*****")
    return BudgetListResponse(data=budgets)

