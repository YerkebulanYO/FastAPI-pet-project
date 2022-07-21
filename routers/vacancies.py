import sys, os
sys.path.insert(0, os.path.abspath('..'))


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from exp.database import get_db
from fastapi import HTTPException
from exp import models, schemas


router = APIRouter(
    prefix='/vacancies',
    tags=['Vacancies']
)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowVacancy, response_description='Get a vacancy')
async def get_vacancy(id: int, db: Session = Depends(get_db)):

    vacancy = db.query(models.Vacancy).get(id)

    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f'Vacancy with id {id} doesnt exist'})

    if not vacancy.owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Vacancy doesnt have owner'})

    return vacancy


@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create a vacancy')
async def create_vacancy(request: schemas.Vacancy, db: Session = Depends(get_db)):
    vacancy = models.Vacancy(**request.dict())
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)

    return 'Vacancy is created succesfully'


@router.put('/edit/{id}', status_code=status.HTTP_202_ACCEPTED, response_description='Edit a vacancies')
async def put_vacancy(id: int, request: schemas.Vacancy, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == id)

    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Vacancy not found'})

    vacancy.update(request.dict(), synchronize_session=False)
    db.commit()

    return 'Vacancy is edited successfully'


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, response_description='Delete a vacancy')
async def delete_vacancy(id: int, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == id)

    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Vacancy not found'})

    vacancy.delete(synchronize_session=False)
    db.commit()

    return 'Vacancy is deleted successfully'



