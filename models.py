import sys, os
sys.path.insert(0, os.path.abspath('..'))

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from database import Base
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = 'employees'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    position = Column(String) #choices
    email = Column(String)
    password = Column(String, nullable=False)

    resumes = relationship('Resume', backref='employees')


class Company(Base):
    __tablename__ = 'companies'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String, nullable=False)

    vacancies = relationship('Vacancy', backref='companies')


class Vacancy(Base):
    __tablename__ = 'vacancies'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    salary = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship('Company')


class Resume(Base):
    __tablename__ = 'resumes'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    phone = Column(Integer)
    email = Column(String)
    city = Column(String)
    salary = Column(Integer, nullable=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))

    employee = relationship('Employee')


class Image(Base):
    __tablename__ = 'images'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    size = Column(BigInteger)
    mime_type = Column(String)
