import sys, os
sys.path.insert(0, os.path.abspath('..'))


from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from exp import models, schemas
from exp.database import get_db
from .authentication import get_current_user

router = APIRouter(
    prefix='/employees',
    tags=['Employees']
)


@router.delete('/delete/video/{id}')
async def delete_video(id: int, db: Session = Depends(get_db)):
    file_info = db.query(models.Image).get(id)

    if not file_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'File is not found'})

    try:
        os.remove(f'static/{file_info.name}')
    except Exception as e:
        print(e)

    db.delete(file_info)
    db.commit()

    return 'File is deleted successfully'


@router.post('/upload')
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    with open(f'static/{file.filename}', 'wb') as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()

    new_image = models.Image(
        name=file.filename,
        size=os.path.getsize(f'static/{file.filename}'),
        mime_type=file.content_type
    )

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image


@router.get('/return/{file_id}')
async def return_file(file_id: int, db: Session = Depends(get_db)):
    file_from_db = db.query(models.Image).get(file_id)
    if not file_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'file is not found'})

    file_path = os.path.join('static/' + f'{file_from_db.name}')

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return {'error': 'File not found'}


@router.get('/download')
async def download_file(file_id: int, db: Session = Depends(get_db)):
    file_from_db = db.query(models.Image).get(file_id)

    if file_from_db:
        file_resp = FileResponse('static/' + file_from_db.name,
                                 media_type=file_from_db.mime_type,
                                 filename=file_from_db.name)
        return file_resp












@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowEmployee)
async def get_employee(id: int, user: schemas.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    employee = db.query(models.Employee).get(id)

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'Employee is not found'})

    return employee


# @router.post('/registration', status_code=status.HTTP_201_CREATED, response_description='Register a user')
# async def registration(request: schemas.Employee, db: Session = Depends(get_db)):
#     check_employee = db.query(models.Employee).filter(models.Employee.email == request.email).first()
#     if check_employee:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'Employee with this email is exist'})
#
#     employee = models.Employee(**request.dict())
#     employee.password = Hash.bcrypt(request.password)
#
#     db.add(employee)
#     db.commit()
#     db.refresh(employee)
#
#     return 'Successfully sign-up'

@router.put('/edit', status_code=status.HTTP_202_ACCEPTED)
async def edit_employee(id: int, request: schemas.Employee, db: Session = Depends(get_db), current_user: schemas.Employee = Depends(get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == id)

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': f'Blog with id {id} doesnt exist'})

    employee.update(request.dict(), synchronize_session=False)

    db.commit()

    return 'Employee updated successfully'
