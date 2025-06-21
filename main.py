import sys
import os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, checks, report, csv
app = FastAPI()

origins = ["http://localhost:4200"]
#Gestione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Includo le rotte
app.include_router(login.router, prefix="/api/login", tags=['login'])
app.include_router(checks.router, prefix="/api/check", tags=['checks'])
app.include_router(report.router, prefix="/api/report", tags=['report'])
app.include_router(csv.router, prefix="/api/csv", tags=['csv'])

@app.post("/")
async def root():
    return {"message": "Hello World"}