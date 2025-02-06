import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Zweite Datenbank
DATABASE_PATH_3 = os.path.join(os.getcwd(), 'Business_Analytics-1', 'Aufgabe_Zwei', 'database', 'person.db')
DATABASE_URL_3 = f"sqlite+aiosqlite:///{DATABASE_PATH_3}"
engine_3 = create_async_engine(DATABASE_URL_3, echo=True)
SessionLocal_3 = sessionmaker(autocommit=False, autoflush=False, bind=engine_3, class_=AsyncSession)
Base_3 = declarative_base()


# Modelle für die zweite Datenbank
class arbeitszeitenWeek(Base_3):
    __tablename__ = "arbeitszeitenWeek"
    Country = Column(String, primary_key=True, index=True)
    Week = Column(Integer)
    Hours_Worked = Column(Float)
    # Weitere Spalten...

# Router
router = APIRouter()

# Dependency für die zweite Datenbank
async def get_db_3():
    async with SessionLocal_3() as session:
        yield session


@router.get("/Abteilung")
async def get_arbeitszeiten_days(session: AsyncSession = Depends(get_db_3)):
    """
    Endpoint to get all columns and values from the arbeitszeitenDays table
    :returns: Das ergebnis der Abfrage
    """
    query = select(person.personID, person.ID, person.Name,
                   person.Abteilung, person.Standort, person.Position, person.Projekt)
    result = await session.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {"personID": row[0],
         "ID": row[1],
         "Name": row[2],
         "Abteilung": row[3],
         "Standort": row[4],
         "Position": row[5],
         "Projekt": row[6]

         }
        for row in data
    ]
