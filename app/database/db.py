from sqlmodel import Session, SQLModel, create_engine

from app.config.Settings import get_settings

SETTING = get_settings()

engine = create_engine(
    url=SETTING.database,
    echo=True,
    connect_args={'check_same_thread': False},
)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
