from sqlmodel import Field, SQLModel, create_engine, select


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    done: bool = Field(default=False)
