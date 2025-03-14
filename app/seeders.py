from sqlmodel import Session, select
from app.database import engine, get_session
from fastapi import APIRouter, Depends
from app.models import Categories

def seed_categories(session: Session = Depends(get_session)):
    if session.exec(select(Categories)).first() is None:
        initial_categories = [
            Categories(name="General", is_initial=1),
            Categories(name="Work", is_initial=1),
            Categories(name="Personal", is_initial=1),
            Categories(name="Travel", is_initial=1),
            Categories(name="Food", is_initial=1),
            Categories(name="Entertainment", is_initial=1),
            Categories(name="Shopping", is_initial=1),
            Categories(name="Education", is_initial=1),
            Categories(name="Health", is_initial=1),
            Categories(name="Gifts", is_initial=1),
            Categories(name="Housing", is_initial=1),
            Categories(name="Transportation", is_initial=1),
            Categories(name="Utilities", is_initial=1),
            Categories(name="Savings", is_initial=1),
            Categories(name="Investments", is_initial=1),
            Categories(name="Taxes", is_initial=1),
            Categories(name="Other", is_initial=1),
        ]

        session.add_all(initial_categories)
        session.commit()
        print("Initial categories added.")
    else:
        print("The categories table already contains data. Skipping seeder.")

