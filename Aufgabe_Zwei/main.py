from fastapi import FastAPI
from .backend import endpointsDay, endpointsWeek, endpointsPerson

app = FastAPI()

app.include_router(endpointsDay.router)
app.include_router(endpointsWeek.router)
app.include_router(endpointsPerson.router)
