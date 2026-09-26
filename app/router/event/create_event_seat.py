from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.seat import BulkSeatCreationRequest
from app.services.event import EventService

router = APIRouter()


@router.post("/v1/event/create-seats", status_code=status.HTTP_201_CREATED)
def create_bulk_seats_for_event(request: Request, seat: BulkSeatCreationRequest, current_user=Depends(get_current_user), db: Session=Depends(get_db)):
    eventservice = EventService(db=db)
    result = eventservice.create_event_seats_in_bulk(seat_details=seat, current_user=current_user)
    if not result:
        return "seat creation failed"

    return "success" 

# , response_model=list[SeatCreationResponse]