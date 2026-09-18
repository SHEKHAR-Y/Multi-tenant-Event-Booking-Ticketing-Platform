import pytest

from uuid import UUID, uuid4

from app.repository.event import EventRepository

def test_get_event_by_id_fail(db_session):
    mock_event_id = uuid4()

    eventrepo = EventRepository(db=db_session)
    assert eventrepo.get_event_by_id(mock_event_id) == None

