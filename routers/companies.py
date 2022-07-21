import sys, os
sys.path.insert(0, os.path.abspath('..'))


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from exp import models, schemas
from exp.database import get_db

router = APIRouter(
    prefix='/companies',
    tags=['Companies']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_companies(db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()

    return companies

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowCompany, response_description='Get a company by id')
async def get_company(id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).get(id)

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f'Company with id {id} doesnt found'})

    return company


# @router.post('/registration', status_code=status.HTTP_201_CREATED, response_description='Register a company')
# async def register_company(request: schemas.Company, db: Session = Depends(get_db)):
#     check_company = db.query(models.Company).filter(models.Company.email == request.email).first()
#
#     if check_company:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': f'Company with email {request.email} exist'})
#
#     company = models.Company(**request.dict())
#     company.password = Hash.bcrypt(request.password)
#     db.add(company)
#     db.commit()
#     db.refresh(company)
#
#     return 'Company is created succesfully'


@router.put('/edit/{id}', status_code=status.HTTP_202_ACCEPTED, response_description='Edit a company')
async def put_company(id: int, request: schemas.Company, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == id)

    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'mwssage': f'Company with id {id} doesnt exist'})

    company.update(request.dict())
    db.commit()

    return 'Employee is updated successfully'
