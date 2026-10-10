from contextlib import asynccontextmanager

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CustomIntegrityError, DatabaseUnavailableError


@asynccontextmanager
async def handle_db_error(db: AsyncSession):
    try: 
        yield
    except IntegrityError: 
        await db.rollback()
        raise CustomIntegrityError("constraints violation")
    except OperationalError as e: 
        await db.rollback()
        raise DatabaseUnavailableError("Database unavialable") from e
    except SQLAlchemyError:
        db.rollback()
        raise
    