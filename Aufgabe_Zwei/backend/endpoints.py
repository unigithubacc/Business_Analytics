import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Erste Datenbank
DATABASE_PATH = os.path.join(os.getcwd(), 'backend', 'database', 'arbeitszeiten.db')
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Zweite Datenbank
DATABASE_PATH_2 = os.path.join(os.getcwd(), 'Business_Analytics-1', 'Aufgabe_Zwei', 'database', 'arbeitszeitenWeek.db')
DATABASE_URL_2 = f"sqlite+aiosqlite:///{DATABASE_PATH_2}"
engine_2 = create_async_engine(DATABASE_URL_2, echo=True)
SessionLocal_2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_2, class_=AsyncSession)
Base_2 = declarative_base()

# Modelle für die erste Datenbank
class arbeitszeiten(Base):
    __tablename__ = "arbeitszeiten"
    Country = Column(String, primary_key=True, index=True)
    Year = Column(Integer)
    Average_Monthly_Income = Column(Float)
    # Weitere Spalten...

# Modelle für die zweite Datenbank
class arbeitszeitenWeek(Base_2):
    __tablename__ = "arbeitszeitenWeek"
    Country = Column(String, primary_key=True, index=True)
    Week = Column(Integer)
    Hours_Worked = Column(Float)
    # Weitere Spalten...

# Router
router = APIRouter()

# Dependency für die erste Datenbank
async def get_db():
    async with SessionLocal() as session:
        yield session

# Dependency für die zweite Datenbank
async def get_db_2():
    async with SessionLocal_2() as session:
        yield session

# Endpoint für die erste Datenbank
@router.get("/average-income")
async def get_average_monthly_income(session: AsyncSession = Depends(get_db)):
    query = select(arbeitszeiten.Country, arbeitszeiten.Average_Monthly_Income)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [{"Country": row[0], "Average_Monthly_Income": row[1]} for row in data]

# Endpoint für die zweite Datenbank
@router.get("/hours-worked")
async def get_hours_worked(session: AsyncSession = Depends(get_db_2)):
    query = select(arbeitszeitenWeek.Country, arbeitszeitenWeek.Hours_Worked)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [{"Country": row[0], "Hours_Worked": row[1]} for row in data]

# FastAPI-App
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)