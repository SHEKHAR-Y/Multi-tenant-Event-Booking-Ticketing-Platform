from uuid import UUID

from sqlalchemy.orm import Session

from app.core.db_error_handler import handle_db_error
from app.core.exceptions import EventNotFound, UserNotAuthorized
from app.models.event import Event
from app.models.seat import Seat
from app.models.user import User, UserRole
from app.repository.event import EventRepository
from app.schemas.event import EventCreateRequest
from app.schemas.seat import BulkSeatCreationRequest


class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EventRepository(self.db)

    def create_event_service(self, event: EventCreateRequest, current_user: User) -> Event:

        # check if the user role is organizer
        if current_user.role is not UserRole.ORGANIZER : 
            raise UserNotAuthorized("User not authorized to perform this task")

        # event repo call to create the event
        new_event = Event(
            organizer_id = current_user.id,
            title = event.title,
            description = event.description,
            venue_name = event.venue_name,
            venue_address = event.venue_address,
            start_time = event.start_time,
            end_time = event.end_time 
        )

        with handle_db_error(self.db): 
            self.repo.create_event(new_event)
            self.db.commit()
            self.db.refresh(new_event)

        return new_event

    def create_event_seats_in_bulk(self, current_user: User, seat_details: BulkSeatCreationRequest) -> bool:

        current_user_id = current_user.id
        event_id = seat_details.event_id
        seat_list = seat_details.seats

        # check the current user role 
        if current_user.role is not UserRole.ORGANIZER:
            raise UserNotAuthorized("User not authorized to perform this task")

        # check if the event exist
        with handle_db_error(self.db):
            event = self.repo.get_event_by_id(event_id)
            if event is None:
                raise EventNotFound("no event exist")

        # check if current user is the owner of the 
        if event.organizer_id != current_user.id:
            raise UserNotAuthorized("you're not authorized to perform this task")

        # insert the seats in db
        with handle_db_error(self.db):
            self.repo.creat_seats_for_event(event_id, seat_list)
            self.db.commit()

        return True

    def get_all_events(self) -> list[Event] | None:
        result = self.repo.get_all_events()

        return result

    def get_all_event_seats(self, event_id: str) -> list[Seat] | None:
        id: UUID = UUID(event_id)

        with handle_db_error(db=self.db):
            result = self.repo.get_event_seats(id)
            return result

        return None