from datetime import datetime
from uuid import uuid4

import pytest

from app.models.event import Event
from app.models.user import User, UserRole
from app.repository.event import EventRepository
from app.schemas.seat import SeatDetails


@pytest.mark.asyncio
async def test_create_event(db_session):
    # register a new user
    test_user = User(
            email = "test@test.com",
            hashed_password = "any_valid_password",
            full_name = "test_name"
        )
    db_session.add(test_user)
    await db_session.commit()

    # change the role of the user to organizer
    test_user.role = UserRole.ORGANIZER
    await db_session.flush()

    # create a new event
    test_event = Event(
        organizer_id=test_user.id,
        title="any testing title",
        description="any testing description",
        venue_name="any testing venue",
        venue_address="any testing venue address",
        start_time=datetime.now(),
        end_time=datetime.now(),
    )
    eventrepo = EventRepository(db=db_session)
    result = await eventrepo.create_event(test_event)

    # assert the result
    assert result is not None
    assert result.title == "any testing title"
    assert result.organizer_id == test_user.id

@pytest.mark.asyncio
async def test_get_event_by_id_fail(db_session):
    mock_event_id = uuid4()

    eventrepo = EventRepository(db=db_session)
    result = await eventrepo.get_event_by_id(mock_event_id)
    assert result == None

@pytest.mark.asyncio
async def test_get_event_by_id_success(db_session):
    # register a new user
    test_user = User(
            email = "test@test.com",
            hashed_password = "any_valid_password",
            full_name = "test_name"
        )
    db_session.add(test_user)
    await db_session.flush()

    # change the role of the user to organizer
    test_user.role = UserRole.ORGANIZER
    await db_session.flush()

    # create a new event
    test_event = Event(
        organizer_id=test_user.id,
        title="any testing title",
        description="any testing description",
        venue_name="any testing venue",
        venue_address="any testing venue address",
        start_time=datetime.now(),
        end_time=datetime.now(),
    )

    db_session.add(test_event)
    await db_session.commit()
    await db_session.refresh(test_event)    

    # store the event id and fetch the event throught that id
    eventrepo = EventRepository(db=db_session)
    result = await eventrepo.get_event_by_id(test_event.id)
    assert result.id == test_event.id
    assert result.organizer_id == test_user.id
    assert result.title == test_event.title
    assert result.description == test_event.description
    assert result.venue_address == test_event.venue_address
    assert result.venue_name == test_event.venue_name

@pytest.mark.asyncio
async def test_get_event_by_id_not_found(db_session):
    mock_event_id = uuid4()

    eventrepo = EventRepository(db=db_session)
    result = await eventrepo.get_event_by_id(mock_event_id)

    assert result == None

# test seat creation 
# when correct event id 
@pytest.mark.asyncio
async def test_create_seat_for_event_success(db_session):
    mock_user_id = uuid4()
    # create a new event
    test_event = Event(
        organizer_id=mock_user_id,
        title="any testing title",
        description="any testing description",
        venue_name="any testing venue",
        venue_address="any testing venue address",
        start_time=datetime.now(),
        end_time=datetime.now(),
    )

    db_session.add(test_event)
    await db_session.commit()
    await db_session.refresh(test_event)  

    event_id = test_event.id
 
    mock_seat_list = [
        SeatDetails(row="A", seat_number=1, price=250),
        SeatDetails(row="A", seat_number=2, price=250),
        SeatDetails(row="A", seat_number=3, price=250),
        SeatDetails(row="A", seat_number=4, price=250),
        SeatDetails(row="A", seat_number=5, price=250),
        SeatDetails(row="A", seat_number=6, price=250),
    ]

    eventrepo = EventRepository(db=db_session)
    result = await eventrepo.create_seats_for_event(event_id, mock_seat_list)

    assert result == True