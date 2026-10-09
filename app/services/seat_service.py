from sqlalchemy.orm import Session

from app.core.db_error_handler import handle_db_error
from app.core.exceptions import EventNotFound, SeatNotAvailable
from app.models.user import User
from app.repository.event import EventRepository
from app.repository.seat import SeatRepository
from app.schemas.seat import SeatBookingRequest


class SeatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SeatRepository(self.db)
        self.event_repo = EventRepository(self.db)

    def book_seats_service(self, current_user: User, seats: SeatBookingRequest) -> bool:
        # check if the event exist 
        with handle_db_error(db=self.db):
            if not self.event_repo.get_event_by_id(event_id=seats.event_id):
                raise EventNotFound("event not found")

        # check if the list of ids are avaiable 
        with handle_db_error(db=self.db): 
            if not self.repo.check_seats_available(ids=seats.id_list):
                raise SeatNotAvailable("seat already booked kindly refresh the page to get the available seats")

            # else book the seats by taking the 
            self.repo.book_seats(ids=seats.id_list, user_id=current_user.id, event_id=seats.event_id)

            self.db.commit()

        return True