import sys, os
sys.path.insert(0, os.path.abspath('..'))

from pydantic import BaseModel
from typing import Optional


class Employee(BaseModel):
    username: str
    position: str # можно добавить список позиции
    email: str
    password: str


class Resume(BaseModel):
    title: str
    description: Optional[str] = None
    phone: int
    email: str
    city: str
    salary: Optional[int] = None

    employee_id: int


    class Config:
        orm_mode = True

    # добавь еще сюда file файловый модель


class ShowEmployee(BaseModel):
    username: str
    position: str
    email: str
    resumes: Optional[list[Resume]] = None

    class Config:
        orm_mode = True


class ShowResume(BaseModel):
    title: str
    description: Optional[str] = None
    city: str
    salary: Optional[int] = None

    employee_id: int
    # добавь еще сюда file файловый модель

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


class Company(BaseModel):
    username: str
    email: str
    password: str


class Vacancy(BaseModel):
    title: str
    description: Optional[str] = None
    salary: Optional[str] = None

    owner_id: int

    class Config:
        orm_mode = True
    # class Config:
    #     allow_population_by_field_name = True


class ShowCompany(BaseModel):
    username: str
    email: str
    vacancies: Optional[list[Vacancy]] = None

    class Config:
        orm_mode = True


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    decision: str


class ShowVacancy(BaseModel):
    title: str
    description: Optional[str] = None
    salary: Optional[str] = None

    owner_id: int

    class Config:
        orm_mode = True

    # task: Optional[List[Task]] = None

    # class Config:
    #     arbitrary_types_allowed = True
        # allow_population_by_field_name = True


class employee_login(BaseModel):
    email: str
    password: str

class company_login(BaseModel):
    email: str
    password: str


class image(BaseModel):
    name: str
    size: int
    mime_type: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str








