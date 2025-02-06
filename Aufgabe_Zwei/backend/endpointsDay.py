import os
import re
from turtle import up, update
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Absolute path to the database file
DATABASE_PATH = os.path.join(
    os.getcwd(), 'backend', 'database', 'arbeitszeiten.db'
)

# database URL to the absolute path
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Set up the database connection
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Define the model for your table


class arbeitszeiten(Base):
    """
        Definition der Tabelle arbeitszeiten

    """

    __tablename__ = "arbeitszeiten"

    # Country als Primärschlüssel
    Country = Column(String, primary_key=True, index=True)
    Average_Monthly_Income = Column(Float)


# Initialize the router for FastAPI
router = APIRouter()

# Dependency to get the DB session


async def get_db():
    """
        Dependency um die Datenbankverbindung zu erhalten

    :yield: die Datenbankverbindung
    """

    async with SessionLocal() as session:
        yield session


# OUTDATED
@router.get("/average-income")
async def get_average_monthly_income(session: AsyncSession = Depends(get_db)):
    """
        Endpoint to get Average_Monthly_Income for all Countries

    :returns: Das ergebnis der Abfrage
    """

    query = select(arbeitszeiten.Country,
                   arbeitszeiten.Average_Monthly_Income)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "Country": row[0],
            "Average_Monthly_Income": row[1]
        }
        for row in data
    ]

