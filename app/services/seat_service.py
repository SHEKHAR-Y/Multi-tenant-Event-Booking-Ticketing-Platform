from sqlalchemy.orm import Session

from app.repository.seat import SeatRepository
from app.schemas.seat import SeatBookingRequest
from app.models.user import User

from app.core.db_error_handler import handle_db_error
from app.core.exceptions import SeatNotAvailable

class SeatService():
    def __init__(self, db: Session):
        self.db = db
        self.repo = SeatRepository(self.db)

    def book_seats_service(self, current_user: User, seats: SeatBookingRequest) -> bool:
        # check if the event exist 


        # check if the list of ids are avaiable 
        with handle_db_error(db=self.db): 
            if not self.repo.check_seats_available(ids=seats.id_list):
                raise SeatNotAvailable("seat already booked")

            # else book the seats by taking the 
            self.repo.book_seats(ids=seats.id_list, user_id=current_user.id, event_id=seats.event_id)

            self.db.commit()

        return True