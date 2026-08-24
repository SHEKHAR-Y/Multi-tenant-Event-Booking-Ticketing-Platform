from sqlalchemy.orm import Session

from app.schemas.event import EventCreateRequest
from app.core.security import decode_access_token
from app.repository.user import UserRepository
from app.repository.event import EventRepository
from app.core.exceptions import UserNotFound, UserNotAuthorized
from app.models.user import UserRole
from app.models.event import Event
from app.core.db_error_handler import handle_db_error

def create_event_service(event: EventCreateRequest, token: str, db: Session) -> Event:
    user_repo = UserRepository(db)
    event_repo = EventRepository(db)

    # decode token and extract payload
    payload = decode_access_token(token)

    # from payload extract the user id entered as the subject in the token 
    user_id = payload["sub"]  

    # check if the user exist with the id 
    result = user_repo.get_user_by_id(user_id)

    if result is None:
        raise UserNotFound("User not Found")

    # check if the user role is organizer
    if result.role is not UserRole.ORGANIZER : 
        raise UserNotAuthorized("User not authorized to perform this task")

    # event repo call to create the event
    new_event = Event(
        organizer_id = result.id,
        title = event.title,
        description = event.description,
        venue_name = event.venue_name,
        venue_address = event.venue_address,
        start_time = event.start_time,
        end_time = event.end_time 
    )

    with handle_db_error(db): 
        event_repo.create_event(new_event)
        db.commit()
        db.refresh(new_event)

    return new_event


