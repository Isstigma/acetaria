from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession, create_async_engine
from app.core.config import settings

#connect_args = {"check_same_thread": False}#todo check if some multithreading issue occurs
engine = create_async_engine(settings.db_url, echo=True, pool_size=100)#todo echo=False or make it dependent on env: local or not idk

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

init_models().__await__()

# Create a Session
async_session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=_AsyncSession, 
    autocommit=False,
)


async def get_session() -> _AsyncSession:
    """
    Yield db session 
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        finally:
            await session.close()
