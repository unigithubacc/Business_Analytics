import os
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Database configuration
DATABASE_PATH_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "arbeitszeitenWeek.db")
DATABASE_URL_2 = f"sqlite+aiosqlite:///{DATABASE_PATH_2}"
engine_2 = create_async_engine(DATABASE_URL_2, echo=True)
SessionLocal_2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_2, class_=AsyncSession)
Base_2 = declarative_base()

# Model for the database
def create_week_columns():
    return {f"Week_{i}": Column(Float) for i in range(1, 40)}

class Arbeitszeiten_Tabelle(Base_2):
    __tablename__ = "Arbeitszeiten_Tabelle"
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)

    # Dynamically adding Week_1 to Week_39 columns
    locals().update(create_week_columns())
    
class Personen_Tabelle(Base_2):
    __tablename__ = "Personen_Tabelle"
    personID = Column(Integer, primary_key=True, index=True)
    ID = Column(Integer, index=True)
    Name = Column(String)
    Abteilung = Column(String)
    Standort = Column(String)
    Position = Column(String)
    Projekt = Column(String)


# Dependency for database session
async def get_db_2():
    async with SessionLocal_2() as session:
        yield session
  
# Router setup
router = APIRouter()

# Endpoint to get all data
@router.get("/all-hours-worked")
async def get_all_hours_worked(session: AsyncSession = Depends(get_db_2)):
    query = select(Arbeitszeiten_Tabelle)
    result = await session.execute(query)
    data = result.scalars().all()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "ID": row.ID,
            "Name": row.Name,
            **{f"Week {i}": getattr(row, f"Week_{i}") for i in range(1, 40)}
        }
        for row in data
    ]


@router.get("/Abteilung")
async def get_all_hours_worked(session: AsyncSession = Depends(get_db_2)):
    query = select(Arbeitszeiten_Tabelle, Personen_Tabelle)
    result = await session.execute(query)
    data = result.scalars().all()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "ID": row.ID,
            "Name": row.Name,
            **{f"Week {i}": getattr(row, f"Week_{i}") for i in range(1, 40)}
        }
        for row in data
    ]

@router.get("/Abteilung")
async def get_all_hours_worked(
    session_arbeitszeiten: AsyncSession = Depends(get_db_2),
    session_personen: AsyncSession = Depends(get_db_2)
):
    # Abfrage: Join zwischen Arbeitszeiten_Tabelle und Personen_Tabelle
    query = (
        select(
            Arbeitszeiten_Tabelle.ID,
            Arbeitszeiten_Tabelle.Name,
            Personen_Tabelle.Abteilung,
            Personen_Tabelle.Standort,
            Personen_Tabelle.Position,
            Personen_Tabelle.Projekt,
            *[getattr(Arbeitszeiten_Tabelle, f"Week_{i}") for i in range(1, 40)]
        )
        .join(Personen_Tabelle, Arbeitszeiten_Tabelle.ID == Personen_Tabelle.ID)
    )

    result = await session_arbeitszeiten.execute(query)
    data = result.fetchall()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    # Rückgabeformat anpassen
    return [
        {
            "ID": row.ID,
            "Name": row.Name,
            "Abteilung": row.Abteilung,
            "Standort": row.Standort,
            "Position": row.Position,
            "Projekt": row.Projekt,
            **{f"Week {i}": getattr(row, f"Week_{i}") for i in range(1, 40)}
        }
        for row in data
    ]