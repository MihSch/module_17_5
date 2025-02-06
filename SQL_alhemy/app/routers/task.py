from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify




router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(get_db : Annotated[Session, Depends(get_db)]):
    tasks = get_db.scalars(select(Task))
    return tasks

@router.get('/task_id')
async def task_by_id(task_id:int, get_db : Annotated[Session, Depends(get_db)]):
    task = get_db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
        return task

@router.post('/create')
async def create_task(get_db : Annotated[Session, Depends(get_db)], task: CreateTask, user_id: int) -> dict:
    if not get_db.scalar(select(User.id).where(User.id == user_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')
    task_dict = dict(task)
    task_dict['slug'] = slugify(task.title)
    task_dict['user_id'] = user_id
    get_db.execute(insert(Task), task_dict)
    get_db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_task(update: UpdateTask, task_id : int, get_db : Annotated[Session, Depends(get_db)]):
    up_task = get_db.scalars(select(Task).where(Task.id == task_id)).first()
    if up_task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    get_db.execute(update(Task).where(Task.id == task_id).values(
        title=up_task.title,
        content=up_task.content
    ))
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete('/delete')
async def delete_task(task_id : int, get_db : Annotated[Session, Depends(get_db)]):
    del_task = get_db.scalars(select(Task).where(Task.id == task_id)).first()
    if del_task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    get_db.execute(delete(Task).where(Task.id == task_id))
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}