from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.event import EventService

router = APIRouter()


@router.get("/v1/event/seats", status_code=status.HTTP_200_OK)
def get_event_seats(request: Request, event_id: str, db: Session = Depends(get_db)):
    eventservice = EventService(db=db)

    return eventservice.get_all_event_seats(event_id=event_id)