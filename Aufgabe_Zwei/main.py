from fastapi import FastAPI
from .backend import endpointsDay, endpointsWeek

app = FastAPI()

app.include_router(endpointsDay.router)
app.include_router(endpointsWeek.router)

