from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os

from models import Base, User
from schemas import UserCreate, UserRead
from db import get_db

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/usersdb")

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist
    from db import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check for existing email (API-side prevention)
    q = await db.execute(
        User.__table__.select().where(User.email == user_in.email)
    )
    existing_user = q.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    # Create new user
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return UserRead.from_orm(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

@app.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(User.__table__.select())
    users = result.fetchall()
    return [UserRead.from_orm(u) for u in [row for row in users]]
