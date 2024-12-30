from datetime import datetime

from sqlmodel import Field, SQLModel, UniqueConstraint


class UserBase(SQLModel):
    name: str = None
    username: str
    __able_args__ = (UniqueConstraint('username'),)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=datetime.now,
    )
    updated_at: datetime | None = Field(
        default_factory=datetime.now,
        sa_column_kwargs={'onupdate': datetime.now},
    )


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
