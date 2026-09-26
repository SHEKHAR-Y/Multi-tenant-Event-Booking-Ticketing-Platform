from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import CustomIntegrityError, DatabaseUnavailableError


@contextmanager 
def handle_db_error(db: Session):
    try: 
        yield
    except IntegrityError: 
        db.rollback()
        raise CustomIntegrityError("constraints violation")
    except OperationalError as e: 
        db.rollback()
        raise DatabaseUnavailableError("Database unavialable") from e
    except SQLAlchemyError:
        db.rollback()
        raise
    