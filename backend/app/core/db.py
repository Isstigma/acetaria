from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

#connect_args = {"check_same_thread": False}#todo check if some multithreading issue occurs
engine = create_engine(settings.db_url, echo=True)#todo echo=False or make it dependent on env: local or not idk

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session