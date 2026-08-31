import pytest

from app.models.user import User, UserRole

from datetime import datetime

def normalize(dt_string):
    # SQLite strips timezone info on round-trip; Postgres (prod) preserves it.
    # Compare as naive datetimes here since only the moment-in-time matters.
    dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
    return dt.replace(tzinfo=None)

def test_create_event_unauthenticated(test_client):
    response = test_client.post(
        "/api/v1/event/create"
        )
    assert response.status_code == 401

def test_create_event_unauthorized(test_client):
    # register a user normally default role = customer 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any testing title",
        "description": "any testing description",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:59.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )
    assert response.status_code == 403 # becuase a user with customer role can't create event only user with role = organizer can create an event        

def test_create_event_authorized_success(test_client, db_session):
    # register normal user 
    test_client.post("/api/v1/register", json={
        "email": "organizer@test.com",
        "username": "organizer_user",
        "password": "anyvalidpassword",
    })

    # use db_session fixture to fetch user, change role 
    user = db_session.query(User).filter(User.email == "organizer@test.com").first()
    user.role = UserRole.ORGANIZER
    db_session.commit()

    # login with this user and extract the token
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "organizer@test.com",
            "password": "anyvalidpassword"
        } 
        )

    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any testing title",
        "description": "any testing description",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:59.198Z"
    }

    create_event_response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )

    assert create_event_response.status_code == 201
    data = create_event_response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["venue_name"] == payload["venue_name"]
    assert data["venue_address"] == payload["venue_address"]
    assert normalize(data["start_time"]) == normalize(payload["start_time"])
    assert normalize(data["end_time"]) == normalize(payload["end_time"])

def test_create_event_end_time_before_start_time(test_client, db_session):
    # register normal user 
    test_client.post("/api/v1/register", json={
        "email": "organizer@test.com",
        "username": "organizer_user",
        "password": "anyvalidpassword",
    })

    # use db_session fixture to fetch user, change role 
    user = db_session.query(User).filter(User.email == "organizer@test.com").first()
    user.role = UserRole.ORGANIZER
    db_session.commit()

    # login with this user and extract the token
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "organizer@test.com",
            "password": "anyvalidpassword"
        } 
        )

    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any testing title",
        "description": "any testing description",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    create_event_response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )

    assert create_event_response.status_code == 422


def test_create_event_title_too_short(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "xx",
        "description": "any testing description",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )
    assert response.status_code == 422

def test_create_event_title_too_long(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    payload = {
        "title": "x" * 101,
        "description": "any testing description",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
                "Authorization": f"Bearer {token}"
            }
        )
    assert response.status_code == 422



def test_create_event_description_too_short(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any valid title",
        "description": "invalid",
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )
    assert response.status_code == 422

def test_create_event_description_too_long(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    payload = {
        "title": "any valid title",
        "description": "a" * 1001,
        "venue_name": "any testing venue",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
                "Authorization": f"Bearer {token}"
            }
        )
    assert response.status_code == 422


def test_create_event_venue_name_too_short(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any valid title",
        "description": "any valid description",
        "venue_name": "x",
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )
    assert response.status_code == 422

def test_create_event_venue_name_too_long(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    payload = {
        "title": "any valid title",
        "description": "any valid description",
        "venue_name": "x" * 101,
        "venue_address": "any testing venue address", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
                "Authorization": f"Bearer {token}"
            }
        )
    assert response.status_code == 422


def test_create_event_venue_address_too_short(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    # test the event creation using the token from login
    payload = {
        "title": "any valid title",
        "description": "any valid description",
        "venue_name": "any testing venue",
        "venue_address": "xxxx", 
        "start_time": "2026-08-30T17:04:58.198Z",
        "end_time": "2026-08-30T17:04:58.198Z"
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
        )
    assert response.status_code == 422

def test_create_event_venue_address_too_long(test_client):
    # register a user normally 
    payload = {
            "email": "test@test.com",
            "username": "test_username",
            "password": "anyvalidpassword",
        }
    test_client.post("/api/v1/register", json=payload)

    # login normally 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com",
            "password": "anyvalidpassword"
        }
        )
    token = login_response.json()["access_token"]

    payload = {
        "title": "any valid title",
        "description": "any valid description",
        "venue_name": "any testing venue",
        "venue_address": "x" * 201,
        "end_time": "2026-08-30T17:04:58.198Z",
        "start_time": "2026-08-30T17:04:58.198Z",
    }

    response = test_client.post(
        "/api/v1/event/create", 
        json=payload,
        headers={
                "Authorization": f"Bearer {token}"
            }
        )
    assert response.status_code == 422

