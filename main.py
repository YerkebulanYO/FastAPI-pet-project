import sys, os

sys.path.insert(0, os.path.abspath('..'))

from fastapi import FastAPI
from database import Base, engine
from routers import users, vacancies, companies, authentication, resumes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(vacancies.router)
app.include_router(companies.router)
app.include_router(authentication.router)
app.include_router(resumes.router)
