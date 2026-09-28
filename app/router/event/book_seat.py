from fastapi import APIRouter, Request, status, Response, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.seat import SeatBookingRequest
from app.services.seat_service import SeatService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/v1/book-seats", status_code=status.HTTP_202_ACCEPTED)
def book_seats(request: Request, seats: SeatBookingRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    seatservice = SeatService(db=db)

    result = seatservice.book_seats_service(current_user, seats=seats)