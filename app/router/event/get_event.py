# get all the events
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.event import EventService

router = APIRouter()

# get list of events
@router.get("/v1/event/get-all", status_code=status.HTTP_200_OK)
def get_all_events(request: Request, db:Session =Depends(get_db)):
    eventservice = EventService(db=db)

    result = eventservice.get_all_events()
    return result 

