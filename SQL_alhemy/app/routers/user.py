from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(get_db : Annotated[Session, Depends(get_db)]):
    users = get_db.scalars(select(User))
    return users

@router.get('/user_id')
async def user_by_id(user_id:int, get_db : Annotated[Session, Depends(get_db)]):
    user = get_db.scalars(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
        return user

@router.post('/create')
async def create_user(create: CreateUser, get_db : Annotated[Session, Depends(get_db)]):
    get_db.execute(insert(User).values(
        username=create.username,
        firstname=create.firstname,
        lastname=create.lastname,
        age=create.age,
        slug=slugify(create.username)))
    get_db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_user(update: UpdateUser, user_id : int , get_db : Annotated[Session, Depends(get_db)]):
    up_user = get_db.scalars(select(User).where(User.id == user_id)).first()
    if up_user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    get_db.execute(update(User).where(User.id == user_id).values(
        firstname=up_user.firstname,
        lastname=up_user.lastname,
        age=up_user.age
    ))
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete('/delete')
async def delete_user(user_id : int, get_db : Annotated[Session, Depends(get_db)]):
    del_user = get_db.scalars(select(User).where(User.id == user_id)).first()
    if del_user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    get_db.execute(delete(User).where(User.id == user_id))
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}