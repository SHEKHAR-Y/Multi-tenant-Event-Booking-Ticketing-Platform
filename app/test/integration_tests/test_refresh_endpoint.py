import pytest 

from app.models.user import User

def test_refresh_token_no_token_provided(test_client):
    # call refresh endpoint without providing refresh token
    refresh_request_response = test_client.post("/api/v1/refresh_access_token")
    assert refresh_request_response.status_code == 422

def test_refresh_token_empty_string(test_client):
    refresh_request_payload = {"refresh_token": ""}

    refresh_request_response = test_client.post("/api/v1/refresh_access_token", json=refresh_request_payload)
    assert refresh_request_response.status_code == 401

def test_refresh_token_for_user_not_exist(test_client, db_session):
    # register user
    payload = {
                "email": "test@test.com",
                "username": "test_username",
                "password": "anyvalidpassword",
            }
    response1 = test_client.post("/api/v1/register", json=payload)
    assert response1.status_code == 201

    # login user 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com", 
            "password": "anyvalidpassword"
            }
        )
    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    # delete the user to check the user not found 
    db_session.query(User).filter(User.email == payload["email"]).delete()
    db_session.commit()

    refresh_request_payload = {"refresh_token": refresh_token}
    refresh_endpoint_response = test_client.post(
        "/api/v1/refresh_access_token",
        json=refresh_request_payload
    )
    
    assert refresh_endpoint_response.status_code == 404

def test_refresh_token_success(test_client):
    # register user
    payload = {
                "email": "test@test.com",
                "username": "test_username",
                "password": "anyvalidpassword",
            }
    response1 = test_client.post("/api/v1/register", json=payload)
    assert response1.status_code == 201

    # login user 
    login_response = test_client.post(
        "/api/v1/login",
        data={
            "username": "test@test.com", 
            "password": "anyvalidpassword"
            }
        )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    refresh_token = login_response.json()["refresh_token"]

    assert access_token != refresh_token

    refresh_request_payload = {"refresh_token": refresh_token}
    refresh_endpoint_response = test_client.post(
        "/api/v1/refresh_access_token",
        json=refresh_request_payload
    )

    assert refresh_endpoint_response.status_code == 201

