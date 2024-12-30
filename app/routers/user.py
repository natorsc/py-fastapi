from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.config.Settings import get_settings
from app.database.db import get_session
from app.models.user import User, UserCreate, UserPublic, UserUpdate

session = get_session()
settings = get_settings()

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix=f'/api/{settings.version}', tags=['users'])


@router.get('/users', response_model=list[UserPublic])
async def read_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.post('/users', response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    hero = session.get(User, user_id)
    if not hero:
        raise HTTPException(status_code=404, detail='User not found')
    return hero


@router.patch('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='Hero not found')
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/users/{user_id}')
def delete_hero(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    session.delete(user)
    session.commit()
    return {'ok': True}
