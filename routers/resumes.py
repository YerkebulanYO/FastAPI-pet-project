import sys, os
sys.path.insert(0, os.path.abspath('..'))


from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from exp import models, schemas
from exp.database import get_db

router = APIRouter(
    prefix='/resumes',
    tags=['Resumes']
)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowResume, response_description='Getting resume')
async def get_resume(id: int, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).get(id)

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f'Resume with id {id} not found'})

    return resume


@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create a resume')
async def create_resume(request: schemas.Resume, db: Session = Depends(get_db)):
    resume = models.Resume(**request.dict())

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return 'Resume is created successfully'


@router.put('/edit/{id}', status_code=status.HTTP_202_ACCEPTED, response_description='Edit a resume')
async def put_resume(id: int, request: schemas.Resume, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == id)
    resume.update(request.dict(), synchronize_session=False)

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Resume is not found'})

    db.commit()

    return 'Resume is updated successfully'


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, response_description='Delete a resume')
async def delete_resume(id: int, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == id)

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Resume is not found'})

    if not resume.employee_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Resume doesnt have owner'})

    resume.delete(synchronize_session=False)
    db.commit()

    return 'Resume is deleted successfully'

