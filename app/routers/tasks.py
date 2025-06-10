from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models.tasks import Task

router = APIRouter()


@router.get('/tasks/', tags=['tasks'])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(Task).offset(offset).limit(limit)).all()


@router.post('/tasks/', tags=['tasks'])
def create_tasks(*, session: Session = Depends(get_session), task: Task):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.put('/tasks/{task_id}', tags=['tasks'])
def update_task(
    *, session: Session = Depends(get_session), task_id: int, task: Task
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete('/tasks/{task_id}', tags=['tasks'])
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    session.delete(task)
    session.commit()
    return {'ok': True}
