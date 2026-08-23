from contextlib import contextmanager

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from app.core.exceptions import DatabaseUnavailableError, CustomIntegrityError

@contextmanager 
def handle_db_error(db: Session):
    try: 
        yield
    except IntegrityError as e: 
        db.rollback()
        raise CustomIntegrityError("constraints violation")
    except OperationalError as e: 
        db.rollback()
        raise DatabaseUnavailableError("Database unavialable") from e
    except SQLAlchemyError as e:
        db.rollback()
        raise
    