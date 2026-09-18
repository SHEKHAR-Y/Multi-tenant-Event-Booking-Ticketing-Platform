from sqlalchemy.orm import Session

import uuid 

from app.core.security import decode_access_token
from app.core.exceptions import UserNotFound, UserNotAuthorized, EventNotFound
from app.core.db_error_handler import handle_db_error

from app.schemas.event import EventCreateRequest
from app.schemas.seat import BulkSeatCreationRequest

from app.repository.user import UserRepository
from app.repository.event import EventRepository

from app.models.user import UserRole, User
from app.models.event import Event

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event_service(self, event: EventCreateRequest, current_user: User) -> Event:
        event_repo = EventRepository(self.db)

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
            event_repo.create_event(new_event)
            self.db.commit()
            self.db.refresh(new_event)

        return new_event

    def create_event_seats_in_bulk(self, current_user: User, seat_details: BulkSeatCreationRequest) -> bool:
        event_repo = EventRepository(self.db)

        current_user_id = current_user.id
        event_id = seat_details.event_id
        seat_list = seat_details.seats

        # check the current user role 
        if current_user.role is not UserRole.ORGANIZER:
            raise UserNotAuthorized("User not authorized to perform this task")

        # check if the event exist
        event = event_repo.get_event_by_id(event_id)
        if event is None:
            raise EventNotFound("no event exist")

        # check if current user is the owner of the 
        if event.organizer_id != current_user.id:
            raise UserNotAuthorized("you're not authorized to perform this task")

        # insert the seats in db
        with handle_db_error(self.db):
            event_repo.creat_seats_for_event(event_id, seat_list)
            self.db.commit()

        return True