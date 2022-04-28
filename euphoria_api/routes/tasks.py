from typing import List

from fastapi import APIRouter, Depends, HTTPException
from psycopg.rows import class_row

from ..config import get_env_config
from ..databases.connections import PostgresConnection
from ..databases.tasks import TasksDB
from ..dependencies import auth
from ..models.tasks import TaskCreate, TaskOut

config = get_env_config('development')

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    dependencies=[Depends(auth)],
    responses={
        404: {'description': 'Not found'},
        403: {"description": "Operation forbidden"},
    },
)

connection = PostgresConnection(
    config.POSTGRES_DATABASE_URI, row_factory=class_row(TaskOut)
)
db = TasksDB(connection, table_name='tasks.tasks')


@router.get("/", response_model=List[TaskOut])
async def read_all():
    return db.read_all()


@router.get("/{task_id}", response_model=TaskOut)
async def read_one(task_id: int):
    if not (task := db.read_one(task_id)):
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return task


@router.post("/", response_model=TaskOut)
async def create(task: TaskCreate):
    return db.create(task)


@router.put("/{task_id}", response_model=TaskOut)
async def update(task: TaskOut):
    return db.update(task)


@router.delete("/{task_id}", status_code=204)
async def delete(task_id: int):
    if not db.read_one(task_id):
        raise HTTPException(status_code=404)
    else:
        db.delete(task_id)
        return ''
