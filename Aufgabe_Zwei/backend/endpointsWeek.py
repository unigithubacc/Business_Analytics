import os
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List

# Database configuration
DATABASE_PATH_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "ETL", "arbeitszeitenWeek.db")
DATABASE_URL_2 = f"sqlite+aiosqlite:///{DATABASE_PATH_2}"
engine_2 = create_async_engine(DATABASE_URL_2, echo=True)
SessionLocal_2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_2, class_=AsyncSession)
Base_2 = declarative_base()

# Model for the database
def create_week_columns():
    return {f"Week_{i}": Column(Float) for i in range(1, 41)}

class Arbeitszeiten_Tabelle(Base_2):
    __tablename__ = "Arbeitszeiten_Tabelle"
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)

    # Dynamically adding Week_1 to Week_40 columns
    locals().update(create_week_columns())
    
class combined(Base_2):
    __tablename__ = "combined"
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Abteilung = Column(String)
    Standort = Column(String)
    Position = Column(String)
    Projekt = Column(String)

    # Dynamically adding Week_1 to Week_40 columns
    locals().update(create_week_columns())    
    

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

    week_columns = [column.name for column in Arbeitszeiten_Tabelle.__table__.columns if column.name.startswith("Week_")]

    return [
        {
            "ID": row.ID,
            "Name": row.Name,
            **{
                f"Week {i}": (
                    20.87 if row.ID == 9 and i == 1 else  # Für ID 5 Khyalla, Week_40 auf 20 setzen
                    24.87 if row.ID == 5 and i == 40 else  # Für ID 5 Abdurrahim, Week_40 auf 20 setzen
                    80.78 if row.ID == 25 and i == 40 else  # Für ID 25 Abdulhalim , Week_40 auf 89.3 setzen                    
                    80.78 if row.ID == 26 and i == 40 else  # Für ID 26 Anil, Week_40 auf 89.3 setzen
                    getattr(row, f"Week_{i}")  # Standardwert aus der DB
                )
                for i in range(1, 41) if f"Week_{i}" in week_columns
            }
        }
        for row in data
    ]


@router.get("/Abteilung")
async def get_all_hours_worked(session: AsyncSession = Depends(get_db_2)):
    query = select(combined)
    result = await session.execute(query)
    data = result.scalars().all()

    if not data:
        raise HTTPException(status_code=404, detail="No data found.")

    return [
        {
            "ID": row.ID,
            "Name": row.Name,
            "Abteilung": row.Abteilung,
            "Standort": row.Standort,
            "Position": row.Position,
            "Projekt": row.Projekt,
            **{
                f"Week {i}": (
                    20.87 if row.ID == 9 and i == 1 else  # Für ID 9, Week_1 auf 20.87 setzen
                    24.87 if row.ID == 5 and i == 40 else  # Für ID 5, Week_40 auf 24.87 setzen
                    80.78 if row.ID == 25 and i == 40 else  # Für ID 25, Week_40 auf 80.78 setzen                    
                    80.78 if row.ID == 26 and i == 40 else  # Für ID 26, Week_40 auf 80.78 setzen
                    getattr(row, f"Week_{i}")  # Standardwert aus der DB
                )
                for i in range(1, 41)
            }
        }
        for row in data
    ]
