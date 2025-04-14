from sqlmodel import create_engine, text,SQLModel
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from src.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
import ssl
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

ssl_context = ssl.create_default_context()
# AsyncEngine is a wrapper around the SQLAlchemy engine that allows you to use it with async/await syntax.
engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL.replace("sslmode=require", ""),
    # echo=True,
    connect_args={
        "ssl":ssl_context
    }
    ))


async def init_db():
    async with engine.begin() as conn:
        # # Use text() to create a textual SQL string representing a SQL statement.
        # statement = text("SELECT 'hello';")
        
        # result = await conn.execute(statement)
        
        # print(result.all())
        
        await conn.run_sync(SQLModel.metadata.create_all)
        

# define session
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with Session() as session:
        yield session