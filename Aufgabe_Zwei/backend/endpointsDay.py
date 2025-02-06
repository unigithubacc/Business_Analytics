import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from typing import List

# Absolute path to the database file
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "arbeitszeitenDays.db")

# Database URL to the absolute path
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Set up the database connection
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Define the model for your table


class ArbeitszeitenDays(Base):
    """
    Definition der Tabelle arbeitszeitenDays
    """
    __tablename__ = "Arbeitszeiten_Tabelle"

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Monday = Column(Float)
    Tuesday = Column(Float)
    Wednesday = Column(Float)
    Thursday = Column(Float)
    Friday = Column(Float)
    Week = Column(Float)


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

# Endpoint to get all columns and values from the arbeitszeitenDays table


@router.get("/arbeitszeiten-days")
async def get_arbeitszeiten_days(session: AsyncSession = Depends(get_db)):
    """
    Endpoint to get all columns and values from the arbeitszeitenDays table
    :returns: Das ergebnis der Abfrage
    """
    query = select(ArbeitszeitenDays.ID, ArbeitszeitenDays.Name, ArbeitszeitenDays.Monday,
                   ArbeitszeitenDays.Tuesday, ArbeitszeitenDays.Wednesday, ArbeitszeitenDays.Thursday, ArbeitszeitenDays.Friday, ArbeitszeitenDays.Week)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {"ID": row[0],
         "Name": row[1],
         "Monday": row[2],
         "Tuesday": row[3],
         "Wednesday": row[4],
         "Thursday": row[5],
         "Friday": row[6],
         "Week": row[6]

         }
        for row in data
    ]
