import sys, os
sys.path.insert(0, os.path.abspath('..'))


from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from exp import models, schemas
from exp.database import get_db
from sqlalchemy.orm import Session
from exp.hashing import bcrypt, verify
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError

SECRET_KEY = 'b430b871ac51f9b85719afb81f83cbc4'
ALGORITHM = 'HS256'
ACCESS_TIME = 10000


router = APIRouter(
    tags=['Authentication']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.Employee).filter(models.Employee.username == username).first()
    if not user:
        return False
    if not verify(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Employee).filter(models.Employee.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TIME)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/token", response_model=schemas.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TIME)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.ShowEmployee)
async def read_users_me(current_user: schemas.ShowEmployee = Depends(get_current_user)):
    return current_user

#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     error = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='You dont authorized',
#         headers={'WWW-Authenticate': 'Bearer'},
#     )
#
#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#         )
#         username: str = payload.get('sub')
#
#         if username is None:
#             raise error
#         token_data = schemas.TokenData(username=username)
#
#     except JWTError:
#         raise error
#
#     user = db.query(models.Employee).filter(username=token_data.username)
#
#     if user is None:
#         raise error
#
#     return user
#
#
# @router.get('/me', response_model=schemas.Employee)
# async def read_me(current_user: schemas.Employee = Depends(get_current_user)):
#     return current_user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#
#     to_encode.update({'exp': expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def authenticate(username: str, password: str, db: Session):
#     user = db.query(models.Employee).filter(models.Employee.username == username).first()
#
#     if not user:
#         return False
#
#     if not verify(password, user.password):
#         return False
#
#     return user
#
#
# @router.post('/login/employee', response_model=schemas.Token)
# async def login_employee(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate(username=form_data.username, password=form_data.password, db=db)
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=ACCESS_TIME)
#     access_token = create_access_token(
#         data={'sub': user.username}, expires_delta=access_token_expires
#     )
#
#     return {
#         'access_token': access_token,
#         'token_type': 'bearer',
#     }










@router.post('/login/company')
async def login_company(request: schemas.company_login, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.email == request.email).first()

    if not company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': f'This company with email {request.email} doesnt exist'})\

    if not verify(company.password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'Uncorrect password'})

    return company


@router.post('/registration_company', status_code=status.HTTP_201_CREATED, response_description='Register a company')
async def register_company(request: schemas.Company, db: Session = Depends(get_db)):
    check_company = db.query(models.Company).filter(models.Company.email == request.email).first()

    if check_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': f'Company with email {request.email} exist'})

    company = models.Company(**request.dict())
    company.password = bcrypt(request.password)
    db.add(company)
    db.commit()
    db.refresh(company)

    return 'Company is created successfully'


@router.post('/registration_employee', status_code=status.HTTP_201_CREATED, response_description='Register a user')
async def registration(request: schemas.Employee, db: Session = Depends(get_db)):
    check_employee = db.query(models.Employee).filter(models.Employee.username == request.username).first()
    if check_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': 'Employee with this email already exists'})

    employee = models.Employee(**request.dict())
    employee.password = bcrypt(request.password)

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return 'Successfully sign-up'
