from collections.abc import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import get_settings

DB_URL = get_settings().database_url

engine = create_async_engine(
    str(DB_URL),
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=300,
    pool_pre_ping=True
    )

class Base(DeclarativeBase):
    pass

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    class_=AsyncSession,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session