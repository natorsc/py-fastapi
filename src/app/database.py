from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

settings = get_settings()


connect_args = {'check_same_thread': False}
engine = create_engine(
    settings.database_url,
    echo=settings.echo,
    connect_args=connect_args,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
