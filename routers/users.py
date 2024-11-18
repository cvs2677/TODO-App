from ..database import SessionLocal
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from ..models import Users
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == int(user.get('id'))).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == int(user.get('id'))).first()

    if not bcrypt_context.verify(user_verification.password, str(user_model.password)):
        raise HTTPException(status_code=401, detail='Incorrect password.')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(phone_number: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == int(user.get('id'))).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
